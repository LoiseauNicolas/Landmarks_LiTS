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

![alt text](https://github.com/LoiseauNicolas/Landmarks_LiTS/tree/main/Images/SlicerIGTLogo.png?raw=true)
