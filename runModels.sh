#!/bin/bash

inputPath=$1

#allData=("RobTetley" "AlejandraGuzman" "RiciBarrientos/NubG4-UASmyrGFP_Control" "RiciBarrientos/NubG4-UASmyrGFP-UASMbsRNAi" "RiciBarrientos/NubG4-UASmyrGFP-UASRokRNAi" "RiciBarrientos/CLS1" "RiciBarrientos/UpsideDown_CorrectedPhotobleaching" "RiciBarrientos/CellCycle")

allData=("data/")

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

len=${#allData[@]}

evalParam="AdaptedRandError"

for (( numData=0; numData<$len; numData++ ))
do
	echo "#${allData[numData]}"
	currentPath=$inputPath/${allData[numData]}/
	learningRateParams="0.0005" # different parameter per method
	weightDecayParams="0.0001"

	weightDecay=($weightDecayParams)
	learningRate=($learningRateParams)

	# Instance segmentation
	List="BCEDiceLoss"
	arrayMethods=($List)

	for numMethod in {0..0}
	do 
		echo "##${arrayMethods[numMethod]}"
		if [ ${weightDecay[numMethod]} != -1 ]; then
			
			newCurrentPath = $currentPath/loss_${arrayMethods[numMethod]}_eval_${evalParam}_${learningRate[numMethod]}_${weightDecay[numMethod]}
			mkdir "$newCurrentPath"

			if [ ! -d "$newCurrentPath" ]; then
				
				sed -e "s@lossMethod@${arrayMethods[numMethod]}@g" \
				 -e "s@evalMethod@${evalParam}@g" \
				 -e "s@currentPath@${currentPath}@g" \
				 -e "s@weightDecay@${weightDecay[numMethod]}@g" \
				 -e "s@learningRate@${learningRate[numMethod]}@g" \
				 $DIR/fineTuneModel_generic.yaml > $DIR/Models/Temp.yaml

				train3dunet --config $DIR/Models/Temp.yaml > out.log

				predict3dunet --config $DIR/Models/Temp.yaml > out.log
			fi
		fi
		echo "##${arrayMethods[numMethod]} - Done!"
	done
	echo "#${allData[numData]} - Done!"
done
