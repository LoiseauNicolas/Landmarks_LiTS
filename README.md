# Landmarks_LiTS
Placement des landmarks sur la base de données LiTS

## Slicer 3D

Installation de slicer3D sous fedora:
- Télécharger à l'adresse suivante: https://download.slicer.org/
https://download.slicer.org/bitstream/60add706ae4540bf6a89bf98
- tar xzvf ./Slicer-4.11.20210226-linux-amd64.tar.gz -C ./path
cd ./Slicer
./Slicer

En cas de problème du type 
"/u/software/slicer/Slicer-4.11.20200930-linux-amd64/bin/SlicerApp-real: error while loading shared libraries: libnsl.so.1: cannot open shared object file: No such file or directory":

cd ./pathtoslicer/Slicer/lib/Slicer-X.Y/
rm libcrypto.so.1.1

### Extension
Dans slicer 3D, ajouter l'extension Slicer IGT, avec le bouton extension manager, dont voici l'icone:

![alt text](https://github.com/LoiseauNicolas/Landmarks_LiTS/blob/main/Images/SlicerIGTLogo.png?raw=true)


## LiTS database
https://competitions.codalab.org/competitions/17094

Volumes abdomen:
[28-45, 72, 129]
Volumes abdomen-pelvis:
[0,2-3,5-8,10-12,19-21,23-26,53-67,69-82,84-86,96-103,128,130]
Volumes thorax-abdomen-pelvis:
[1,4,13-18,22,27,48-52,68,83,87-95,104-127]
Volumes avec problèmes de spacing:
[9,46-47]