#!/bin/bash

inputPath=$1

#allData=("RobTetley" "AlejandraGuzman" "RiciBarrientos/NubG4-UASmyrGFP_Control" "RiciBarrientos/NubG4-UASmyrGFP-UASMbsRNAi" "RiciBarrientos/NubG4-UASmyrGFP-UASRokRNAi" "RiciBarrientos/CLS1" "RiciBarrientos/UpsideDown_CorrectedPhotobleaching" "RiciBarrientos/CellCycle")

allData=("data/")

pretrainedModel=$2 

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

len=${#allData[@]}
for (( numData=0; numData<$len; numData++ ))
do
	echo "#${allData[numData]}"
	currentPath=$inputPath/${allData[numData]}/$pretrainedModel/
	probabilityThreshold="0.75 -1 -1 -1" # different parameter per method
	betaParameters="0.3 -1 -1 -1"

	betaParam=($betaParameters)
	probThresh=($probabilityThreshold)

	# Instance segmentation
	List="GASP MutexWS DtWatershed MultiCut"
	arrayMethods=($List)

	for numMethod in {0..3}
	do 
		echo "##${arrayMethods[numMethod]}"
		if [ ${betaParam[numMethod]} != -1 ]; then
			if [ ! -d "$currentPath/${arrayMethods[numMethod]}_${probThresh[numMethod]}_${betaParam[numMethod]}" ]; then
				
				sed -e "s@currentMethod@${arrayMethods[numMethod]}@g" \
				 -e "s@currentPath@${currentPath}@g" \
				 -e "s@betaParam@${betaParam[numMethod]}@g" \
				 -e "s@probThresh@${probThresh[numMethod]}@g" \
				 $DIR/Models/Generic_InstanceSegmentation.yaml > $DIR/Models/Temp.yaml

				plantseg --config $DIR/Models/Temp.yaml > out.log
				rm $DIR/Models/Temp.yaml
			fi
		fi
		echo "##${arrayMethods[numMethod]} - Done!"
	done
	echo "#${allData[numData]} - Done!"
done
