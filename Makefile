# java -jar DiademMetric.jar -G [GoldStandardFilename] -T [TestReconstructionFilename] -D [data set number]
STACK=1
DATASET_NUM=5

ifdef STK
	STACK=$(STK)
endif

ifdef DSNUM
	DATASET_NUM=$(DSNUM)
endif

runmetric:
	java -jar DiademMetric/DiademMetric.jar -G OlfactoryProjectionFibers/GoldStandardReconstructions/OP_$(STACK).swc -T Test/OP_$(STACK).swc -D $(DATASET_NUM)

clean:
	rm -rf ip/__pycache__ && rm -rf ip/.ipynb_checkpoints && rm -rf .ipynb_checkpoints && rm -rf Test/.ipynb_checkpoints

runpypy:
	pypy OP_$(STACK).py

all: runpypy runmetric
	@/usr/bin/time -f "time cpu: %Us\ntime sys: %Ss" -o acc/OP_$(STACK)_acc.txt pypy OP_$(STACK).py
	java -jar DiademMetric/DiademMetric.jar -G OlfactoryProjectionFibers/GoldStandardReconstructions/OP_$(STACK).swc -T Test/OP_$(STACK).swc -D $(DATASET_NUM) >> acc/OP_$(STACK)_acc.txt
	@echo "Done!"