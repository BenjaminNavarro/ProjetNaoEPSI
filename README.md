# ProjetNaoEPSI

Côté hôte ou VM :

Lancer V-REP et changer la scène (file -> open scene) avec Nao (ProjetNAOEPSI/vrep/NAO.ttt)

Côté VM :

Naoqi : 

* cd ~/Prog/naoqi-sdk-2.3.0.14-linux64/bin

* ./naoqi-bin

Bridge VREP : 

* cd ~/Prog/qibuild-workspace/build/naoqi_vrep_bridge/build-naoqi-sdk/sdk/bin

* ./naoqi_vrep_bridge ip_machine_vrep

Example :

* cd ~/Prog/ProjetNaoEPSI/examples

* python test.py

* python cartesian_test.py

* ...

Choregraphe : 457d-1533-542b-551b-6f13-4435-602e-2f10-5e41-5846
