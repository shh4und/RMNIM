# java -jar DiademMetric.jar -G [GoldStandardFilename] -T [TestReconstructionFilename] -D [data set number]
STACK=OP_1
DATASET_NUM=5

ifdef STK
	STACK=$(STK)
endif

ifdef DSNUM
	DATASET_NUM=$(DSNUM)
endif

acc:
	java -jar DiademMetric/DiademMetric.jar -G OlfactoryProjectionFibers/GoldStandardReconstructions/$(STACK).swc -T Test/$(STACK).swc -D $(DATASET_NUM)

clean:
	rm -rf ip/__pycache__ && rm -rf ip/.ipynb_checkpoints && rm -rf .ipynb_checkpoints 

runpypy:
	pypy $(STACK).py

all: runpypy acc
	@/usr/bin/time -f "time cpu: %Us\ntime sys: %Ss" -o acc/$(STACK)_acc.txt pypy $(STACK).py
	java -jar DiademMetric/DiademMetric.jar -G OlfactoryProjectionFibers/GoldStandardReconstructions/$(STACK).swc -T Test/$(STACK).swc -D $(DATASET_NUM) >> acc/$(STACK)_acc.txt
	@echo "Done!"