# java -jar DiademMetric.jar -G [GoldStandardFilename] -T [TestReconstructionFilename] -D [data set number]
STACK=1
DATASET=5
TEST=$(STACK)
GOLD=$(STACK)

runmetric:
	java -jar DiademMetric/DiademMetric.jar -G OlfactoryProjectionFibers/GoldStandardReconstructions/OP_$(GOLD).swc -T Test/OP_$(TEST).swc -D $(DATASET)

clean:
	rm -rf ip/__pycache__ && rm -rf ip/.ipynb_checkpoints && rm -rf .ipynb_checkpoints && rm -rf Test/.ipynb_checkpoints

runpypy:
	pypy OP_$(STACK).py

all: 
	@/usr/bin/time -f "time cpu: %Us\ntime sys: %Ss" -o acc/OP_$(STACK)_acc.txt pypy OP_$(STACK).py
	java -jar DiademMetric/DiademMetric.jar -G OlfactoryProjectionFibers/GoldStandardReconstructions/OP_$(GOLD).swc -T Test/OP_$(TEST).swc -D $(DATASET) >> acc/OP_$(STACK)_acc.txt
	@echo "Done!"

#runcustom:
#    @/usr/bin/time -f "time cpu: %Us\ntime sys: %Ss" -o acc/OP_$(TEST)_acc.txt pypy OP_$(TEST).py
#    java -jar DiademMetric/DiademMetric.jar -G OlfactoryProjectionFibers/GoldStandardReconstructions/OP_$(GOLD).swc -T Test/OP_$(TEST).swc -D $(DATASET)
#    @echo "Done!"