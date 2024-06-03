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
	rm -rf ip/__pycache__ && rm -rf .ipynb_checkpoints
