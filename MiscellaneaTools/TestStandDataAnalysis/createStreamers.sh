#!/bin/bash

# cmsrel CMSSW_15_0_4_patch1 
# cd CMSSW_15_0_4_patch1/src
# cmsenv
# scram b

# Usage: ./createStreamers.sh <RUNNUMBER> <LS>

RUNNUMBER=${1:-392642} # 2025 EphemeralHLTPhysics
LUMISECTION=${2:-174} # 174 - 187

case $LUMISECTION in
  174) INPUTFILES="\
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/06ac627c-f97b-40ed-a279-16fdcf990c2c.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/8ec096b9-1293-4ee7-8e27-369889a521ff.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/e39b2b26-9b68-40e7-8e2d-c259637ea5d3.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/5f25f30f-1372-4875-ac25-0f437f2590be.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/ddcb337e-3536-4361-b69a-02ba755b9eb0.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/e7512b2b-d00a-4d71-924d-9563c2b36c18.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/7dd68eaf-bb9b-456e-9318-961c3903c84a.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/a7b5720c-aa47-4783-b838-dce20b7130ee.root" ;;

  175) INPUTFILES="\
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/c854f400-a6e0-44e5-a658-15dc0fafd27e.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/1fdfbe71-b994-4aa5-98ea-8e3ccc251ed2.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/153820e2-a9b8-451e-a4b4-e1b2a958bc40.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/fdf86a23-6072-4111-a6f2-30f9269430e7.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/72030f53-2c19-4d9d-a063-cc88197ffd72.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/67c61a46-d6a9-47cd-bc74-7b4ea0cba870.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/cee5f398-1034-418d-891a-c5d9a0903678.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/5749c19d-e6fc-4693-8acb-f4c2035708a5.root" ;;

  176) INPUTFILES="\
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/34a8cb24-4f85-4b44-bb2e-727e5d051518.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/972aed97-f20d-4c1f-a86b-0383597a1ea2.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/04e580e5-5eda-436a-acca-4eff56489761.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/f82cf1e4-2960-4edd-af2f-d22af743c810.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/1247f27e-7160-40b2-9d3f-1f9636ad1b53.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/d903b449-92ec-4be7-bcf7-a53df200236f.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/1955843b-bb8c-4a4f-bd2c-ed8780979df8.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/33b25585-b98f-423e-88ae-631a1d801228.root" ;;

  177) INPUTFILES="\
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/ecb9114f-7be9-4158-95c7-1316dd091dae.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/5902d003-41a1-4fe4-89e1-42e08cff53b3.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/41747596-1c7b-4014-846d-3a4aadb27cf1.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/6a3cca94-00d9-48b0-a659-55d1ea596a3a.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/7820190a-ca3a-440e-8018-b7c3b264b558.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/c404c2ec-f610-4793-8b35-208e46ff7c1a.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/33ea0746-c2b4-4ba7-8b7f-36f6d4b5b011.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/5a8be213-014a-47bf-a89a-018d73aab1b6.root" ;;

  178) INPUTFILES="\
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/797476d3-7ca2-4492-a892-3efad0b944bf.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/067bcec4-ae3f-4eb0-90f4-2c21d4993597.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/b071a507-4b73-4048-8356-959be8bfabce.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/e0b50d75-df15-4560-920f-1aa8e2b60717.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/798c6c58-4096-49d3-b261-d5bbb3de736f.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/9d08ffd3-7fbe-4e2a-9dd1-a3558c00fd88.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/d4316081-93fe-4c2e-9530-56515da4fdaa.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/212b5382-cc76-4ef8-a19a-33b1419d99a6.root" ;;

  179) INPUTFILES="\
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/ac0cab58-926b-4157-bf8d-6a78bedd0736.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/e1be484b-0651-427e-ae73-17c2b4be5393.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/379f616c-4f25-4aba-8b6b-3a7625a8c122.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/b182af70-f0ef-47f8-8fba-706e32fc9829.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/369dca5e-988d-43d5-89cf-32821e4e4351.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/38826aa4-033a-47dc-a520-51fdfdc4684c.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/548b4177-19a2-41a1-8dbb-5d969b2eb1de.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/deab5cbe-762c-4dbf-ad1e-3563ea9b0819.root" ;;

  180) INPUTFILES="\
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/15330997-fa91-418d-94ec-0e10325e36ba.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/6a01d68f-89c8-49bf-a500-6413472eaa1b.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/d27b8b53-0689-47a9-ba1c-d66c7e5cf789.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/6b15ccab-39da-4d15-9f9e-03aeaa968f29.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/bd93a93f-0b92-4723-af10-1dddeabe6556.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/bdf666d5-165d-4d6e-a079-f68b5b89bfaf.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/8ab11dd8-9a97-484a-92c1-5609592f1556.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/a1b51385-9495-430a-a43f-dec1b2f34295.root" ;;

  181) INPUTFILES="\
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/623c0e98-b3eb-449b-9499-48c7268b23fc.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/d1d06e40-176a-4157-848c-2fdcf7311367.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/fbe6a1e4-6cc2-4727-9797-dd64e348fbab.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/d2e6f51d-b446-4ac5-bdff-ab32af4703ca.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/4982f5a2-c2e1-418d-b43f-cb6844490276.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/0423bf7c-a5de-42d0-9e79-cb7e829966a8.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/957b1e77-54ce-4936-a465-aaf48d5d48c0.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/1b4f5af7-09d0-47f1-b03b-874dec6d10e8.root" ;;

  182) INPUTFILES="\
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/e7990694-b6e2-4ead-80e0-724c4fb51daa.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/75ef662f-f114-4246-86a0-61b7316914da.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/9d446b54-f431-442d-b3b5-23df07d4a37c.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/67490682-199a-4461-9f1d-01134e38196b.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/b38d85d4-f333-44fe-b032-e67bf6763082.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/254851b7-0e33-4d4d-83ea-f6627126b1dc.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/75c2312d-f3e0-4aba-af7e-f5290bc732bc.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/c5f36f8f-d354-418a-9f0b-7083e490b275.root" ;;

  183) INPUTFILES="\
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/1220b97e-4c64-45ef-afb8-660fa2e3d0c6.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/7674a872-c3a2-4d5c-9fe4-c756b5e94da3.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/2491bcfc-9983-41f2-a90d-77234d2698dc.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/af447460-37e2-4bde-9d77-ed6a12ba6302.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/1af38e3b-e319-498c-9f35-e84c9f6f3525.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/4c964ae5-5d75-42d4-b408-8bf4e0270cda.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/b6b7d826-154f-408f-b6a9-49f6e5ffbf43.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/f619145e-1fd5-43b2-9806-082b7f2010f7.root" ;;

  184) INPUTFILES="\
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/97c29d06-61c5-43ec-9fb3-4edb9d75a86f.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/edfd753c-af07-44e3-a6cf-f209de8dad96.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/81a61da7-c71d-4600-9cea-93dea3cb2330.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/65644d9d-e92e-4685-8bc5-55f0d7940021.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/5a30a45b-2933-4a7e-841a-9ec74ebdb9b8.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/17503271-51a5-409e-bb84-faf06a2b2f26.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/9fed6d6a-a47a-4c31-9c02-33d6022cae83.root 
         root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/316b4c71-6e76-47ba-81c4-891ce6fe7836.root" ;;

  185) INPUTFILES="\
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/d9218823-806a-4790-8ec9-a423d8c74d0a.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/940e1308-cb79-4660-9e47-eb257cd211c1.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/1c0f623c-42b2-4bea-a65b-9b612463b358.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/843ddb2b-4824-4a56-9faf-db60c7f676a6.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/5bf50e24-de99-48eb-909c-a2dff64474b8.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/73b3b21e-ec3e-47b9-a7d5-c948796bc518.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/3a3f3ef7-ca09-4f07-91e7-83ab81253b2e.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/16c4a20b-9b22-4648-91a2-9406ca6fb16d.root" ;;

  186) INPUTFILES="\
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/2ddf6bef-61dc-4eeb-9c5a-30bb8008b8e1.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/c6894e60-f6b1-46fa-ab91-1104d63e53d5.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/0caf7f27-2b64-428b-8bd7-35f0bc401ed9.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/db7d6a1a-f45a-4a03-aee0-a87ea433aa4b.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/b4348d06-b0fa-4560-b3d2-eed2409f205c.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/5de5b502-2540-432d-b236-9f3dbefbc356.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/2e5eda84-2f9b-4c18-99c5-2094242e5df3.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/62988b6f-f3b2-49e4-8a18-6d87467ac998.root" ;;

  187) INPUTFILES="\
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/8de8f2e6-e3e6-43c3-9111-45ef618e4a7a.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/71a4dded-9fbb-4a0f-ba99-7b3b4a324041.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/0bc83155-82c8-4cd9-827f-cbae125f0f57.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/8e87db72-a1f5-4c2a-a7ea-5984aa92a4b6.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/0d290066-627a-42bf-a2b5-27bf8ddf7f52.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/b3544421-09f5-42ca-a18b-8274c6514dae.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/210fa1d0-801e-4a8b-965e-e37a76d250f9.root 
        root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/19e379f6-91c9-44c0-8b5a-69269e20b131.root" ;;

  *) echo "Invalid LS input: ${LUMISECTION}"; exit 1 ;;
esac

echo -e "Processing the following input files from run ${RUNNUMBER} LS ${LUMISECTION}:\n${INPUTFILES}"

rm -rf run${RUNNUMBER}*

# run on 23000 events of given LS, without event limits per input file
convertToRaw -l 23000 -r ${RUNNUMBER}:${LUMISECTION} -o . -- ${INPUTFILES}

tmpfile=$(mktemp)
hltConfigFromDB --configName /users/musich/tests/dev/CMSSW_15_0_0/NGT_DEMONSTRATOR/TestData/online/HLT/V3 > "${tmpfile}"
cat <<@EOF >> "${tmpfile}"
process.load("run${RUNNUMBER}_cff")
# to run without any HLT prescales
del process.PrescaleService
del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.options.numberOfThreads = 32
process.options.numberOfStreams = 32

process.options.wantSummary = True
# # to run using the same HLT prescales as used online
# process.PrescaleService.forceDefault = True
@EOF

edmConfigDump "${tmpfile}" > hlt.py

bash -c 'echo $$ > cmsrun.pid; exec cmsRun hlt.py &> hlt.log'
job_pid=$(cat cmsrun.pid)
echo "cmsRun is running with process ID (PID): ${job_pid}"

# remove input files to save space
rm -f run${RUNNUMBER}/run${RUNNUMBER}_ls0*_index*.*

# prepare the files by concatenating the .ini and .dat files
mkdir -p prepared
cat run${RUNNUMBER}/run${RUNNUMBER}_ls0000_streamLocalTestDataRaw_pid${job_pid}.ini run${RUNNUMBER}/run${RUNNUMBER}_ls0${LUMISECTION}_streamLocalTestDataRaw_pid${job_pid}.dat > prepared/run${RUNNUMBER}_ls0${LUMISECTION}_streamLocalTestDataRaw_pid${job_pid}.dat

# run the FRD conversion
#cmsRun convertStreamerToFRD.py filePrepend=file: inputFiles=prepared/run${RUNNUMBER}_ls0${LUMISECTION}_streamLocalTestDataRaw_pid${job_pid}.dat # NOTE: uncomment to immediately run the conversion to FRD (.raw)
