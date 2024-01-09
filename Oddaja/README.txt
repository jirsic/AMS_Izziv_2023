Za poravnavo: 
python run_registration.py -i_1 "Case_05_CTA_PT00007_20120504.obj" -i_2 "Case_05_CTA_PT00007_20180914.obj" -o "resultMesh.pcd"

Za velikot anevrizme posameznega point clouda:
python run_measurements.py -i "Case_05_CTA_PT00007_20120504.obj" -o "aneurysmSize.csv"

Za razliko velikosti anevrizem dveh point cloudov: 
python run_registration.py -i_1 "Case_05_CTA_PT00007_20120504.obj" -i_2 "Case_05_CTA_PT00007_20180914.obj" -o "aneurysmGrowth.csv"


Koda poskusov segmentacije, slike ter ostali material se nahajajo na:
https://github.com/jirsic/AMS_Izziv_2023