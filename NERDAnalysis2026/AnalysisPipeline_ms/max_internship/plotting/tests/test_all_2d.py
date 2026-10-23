"""Synthetic ROOT integration tests; run with unittest discover -s plotting/tests."""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import uproot
import yaml
import matplotlib.pyplot as plt
from all_1D_ScoutingDQM import All1DPlot
from all_2D_ScoutingDQM import All2DPlot


class All2DTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        config = yaml.safe_load((Path(__file__).resolve().parents[1] / 'config.yaml').read_text())
        config['output']['png_dir'] = str(self.base / 'png')
        config['lumi_csv'] = str(self.base / 'lumi.csv')
        (self.base / 'lumi.csv').write_text('#run:fill,recorded(/pb)\n123:1,1000\n')
        self.x = np.array([0., 1., 3.])
        self.y = np.array([-2., 0., 2., 5.])
        self.a = np.array([[2., 4., 0.], [8., 10., 12.]])
        self.prefix = 'DQMData/Run 123/HLT/Run summary/ScoutingOffline/'
        for c, scale in zip(config['conditions'], [1., 2., 3.]):
            path = self.base / c['label']
            path.mkdir()
            c['path'] = str(path)
            with uproot.recreate(path / 'a.root') as f:
                f[self.prefix + 'Maps/map'] = (self.a * scale, self.x, self.y)
                f[self.prefix + 'Maps/one'] = (self.a.sum(axis=1), self.x)
            with uproot.recreate(path / 'b.root') as f:
                f[self.prefix + 'Maps/map'] = (self.a * scale, self.x, self.y)
                f[self.prefix + 'Later/map'] = (self.a, self.x, self.y)
        self.cfg = self.base / 'config.yaml'
        self.cfg.write_text(yaml.safe_dump(config))

    def plot(self, cls=All2DPlot, **kwargs):
        return cls(config_path=self.cfg, local=True, jobs=1, **kwargs)

    def test_discovery_sum_and_render(self):
        plot = self.plot()
        targets = plot.targets()
        self.assertEqual([t['subpath'] for t in targets], ['Later', 'Maps'])
        plot._preload(targets)
        target = targets[1]
        fetched = plot.fetch(target)
        self.assertEqual([(p[0], p[1]) for p in fetched], list(plot.pairs))
        np.testing.assert_array_equal(fetched[0][2][0], self.a * 6)
        outputs = list(plot.make_figures(target, fetched))
        self.addCleanup(plt.close, 'all')
        self.assertEqual(len(outputs), 6)
        self.assertEqual(len({o.png_name for o in outputs}), 6)
        from matplotlib.backends.backend_pdf import PdfPages
        with PdfPages(self.base / 'test.pdf') as pdf:
            for out in outputs:
                plot._save(out, pdf)
        self.assertEqual(len(list((self.base / 'png').glob('*.png'))), 6)
        self.assertGreater((self.base / 'test.pdf').stat().st_size, 1000)

    def test_missing_lumi_excluded_before_discovery_and_sum(self):
        # Put an uncovered run first in the same file as an accepted run.
        # Its huge contents and unique histogram must never enter the output.
        for label in ('Prompt', 'HLT', 'NGT'):
            with uproot.recreate(self.base / label / 'mixed.root') as f:
                bad = self.prefix.replace('Run 123', 'Run 402839')
                f[bad + 'Maps/map'] = (self.a * 1000, self.x, self.y)
                f[bad + 'Excluded/only_bad_run'] = (self.a, self.x, self.y)
                f[self.prefix + 'Maps/map'] = (self.a, self.x, self.y)
        plot = self.plot()
        warnings = io.StringIO()
        with contextlib.redirect_stderr(warnings):
            targets = plot.targets()
            plot._preload(targets)
            self.assertEqual(plot.runs(), [123])
        self.assertNotIn('Excluded', [t['subpath'] for t in targets])
        np.testing.assert_array_equal(plot._cache[('Prompt', 'Maps/map')][0],
                                      self.a * 3)
        self.assertEqual(plot.source.contributing_runs[('Prompt', 'Maps', 'map')], {123})
        message = warnings.getvalue()
        self.assertEqual(message.count('SKIPPING RUN 402839'), 1)
        for label in ('Prompt', 'HLT', 'NGT'):
            self.assertIn(str(self.base / label / 'mixed.root'), message)
        # Per-run processing also excludes the uncovered run.
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.plot(per_run=True).runs(), [123])
        # Explicit user exclusions are applied before luminosity validation.
        quiet = io.StringIO()
        with contextlib.redirect_stderr(quiet):
            self.assertEqual(self.plot(exclude_runs=[402839]).runs(), [123])
        self.assertEqual(quiet.getvalue(), '')
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'No DQM runs remain with recorded'):
                self.plot(per_run=402839).runs()

    def test_no_lumi_coverage_stops_before_rendering(self):
        csv = self.base / 'empty.csv'
        csv.write_text('#run:fill,recorded(/pb)\n')
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'No DQM runs remain with recorded'):
                self.plot(lumi_csv=str(csv)).targets()
        malformed = self.base / 'malformed.csv'
        malformed.write_text('wrong header\n')
        with self.assertRaisesRegex(ValueError, 'expected brilcalc'):
            self.plot(lumi_csv=str(malformed)).targets()

    def test_profiles_merge_weighted_means_and_project(self):
        from uproot.writing.identify import to_TAxis, to_TProfile2D
        key = 'Muons/Properties/MuonNoVtx_nTrackerLayersWithMeasurement_vs_eta_phi_prof'
        w1 = np.array([[1., 3., 0.], [2., 1., 0.]])
        w2 = np.array([[3., 1., 0.], [1., 2., 0.]])
        m1 = np.array([[2., 4., 0.], [0., 5., 0.]])
        m2 = np.array([[6., 8., 0.], [0., 2., 0.]])

        def flat(a):
            return np.pad(a, 1).T.flatten().astype(float)

        for label, scale in [('Prompt', 1), ('HLT', 2), ('NGT', 3)]:
            for filename, w, m in [('a.root', w1, m1), ('b.root', w2, m2)]:
                sums = m * w * scale
                profile = to_TProfile2D(
                    fName=None, fTitle='tracker layers', data=flat(sums),
                    fEntries=float(w.sum()), fTsumw=float(w.sum()), fTsumw2=float(w.sum()),
                    fTsumwx=0., fTsumwx2=0., fTsumwy=0., fTsumwy2=0., fTsumwxy=0.,
                    fTsumwz=float(sums.sum()), fTsumwz2=0., fSumw2=flat(m*m*w*scale*scale),
                    fBinEntries=flat(w), fBinSumw2=flat(w),
                    fXaxis=to_TAxis('xaxis', '#eta', 2, 0., 3., self.x),
                    fYaxis=to_TAxis('yaxis', '#phi', 3, -2., 5., self.y))
                with uproot.update(self.base / label / filename) as f:
                    f[self.prefix + key] = profile
        plot = self.plot()
        targets = plot.targets()
        target = next(t for t in targets if t['hist_name'].endswith('_prof'))
        plot._preload(targets)
        values = plot._cache[('Prompt', key)][0]
        expected = plot._mean(m1*w1 + m2*w2, w1+w2)
        np.testing.assert_allclose(values, expected)
        self.assertEqual(values[0, 0], 5.)  # unequal weights: not sum/average of means
        self.assertEqual(values[1, 0], 0.)  # measured zero remains valid
        self.assertTrue(np.isnan(values[0, 2]))  # unfilled bin remains undefined
        for axis in (0, 1):
            np.testing.assert_allclose(plot._projection('Prompt', target, values, axis),
                plot._mean((m1*w1+m2*w2).sum(axis=axis), (w1+w2).sum(axis=axis)))
        outputs = list(plot.make_figures(target, plot.fetch(target)))
        self.assertEqual(len(outputs), 6)
        for out in outputs:
            out.fig.canvas.draw()
            plt.close(out.fig)

    def test_math_and_projection_order(self):
        a = np.array([[4., 3.], [5., 2.]])
        b = np.array([[2., 0.], [1., 1.]])
        np.testing.assert_array_equal(All2DPlot.difference(a, b, 'absolute'), a - b)
        rel = All2DPlot.difference(a, b, 'relative')
        self.assertTrue(np.isnan(rel[0, 1]))
        self.assertEqual(rel[1, 0], 4.)
        projected = All2DPlot.difference(a.sum(axis=1), b.sum(axis=1), 'relative')
        np.testing.assert_array_equal(projected, [2.5, 2.5])

    def test_missing_and_mismatched_conditions(self):
        plot = self.plot()
        target = plot.targets()[0]
        key = plot._full_name(target)
        plot._cache = {('NGT', key): [self.a, self.x, self.y],
                       ('Prompt', key): [self.a, self.x + 1, self.y]}
        self.assertIsNone(plot.fetch(target))
        plot._cache[('Prompt', key)][1] = self.x
        self.assertEqual(len(plot.fetch(target)), 1)

    def test_run_selection_and_1d_regression(self):
        plot = self.plot(per_run=123, include=['Maps/'])
        plot._select_run(plot.runs()[0])
        self.assertEqual(len(plot.targets()), 1)
        self.assertIn('All2D_Run123', plot._pdf_name('Maps'))
        one = self.plot(All1DPlot)
        targets = one.targets()
        self.assertEqual(len(targets), 1)
        one._preload(targets)
        fetched = one.fetch(targets[0])
        self.assertEqual(len(fetched[0]['data']), 2)
        outputs = one.make_figures(targets[0], fetched)
        self.assertEqual(len(outputs), 1)
        plt.close(outputs[0].fig)


if __name__ == '__main__':
    unittest.main()
