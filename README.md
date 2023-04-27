# USAGE
## EXCLUSIVE :
cp caches/cache_ex.cc src/cache.cc
## INCLUSIVE :
cp caches/cache_in.cc src/cache.cc
## NON-INCLUSIVE :
cp caches/cache_ni.cc src/cache.cc

# Compile

ChampSim takes seven parameters: Branch predictor, L1I prefetcher, L1D prefetcher, L2C prefetcher, LLC prefetcher, LLC replacement policy, and the number of cores. 
For example, `./build_champsim.sh bimodal no no no next_line lru 1` builds a single-core processor with bimodal branch predictor, no L1 instruction prefetcher, no L1/L2 data prefetchers, ip-stride LLC prefetcher and the baseline LRU replacement policy for the LLC.
```
$ ./build_champsim.sh bimodal no no no next_line lru 1

$ ./build_champsim.sh ${BRANCH} ${L1I_PREFETCHER} ${L1D_PREFETCHER} ${L2C_PREFETCHER} ${LLC_PREFETCHER} ${LLC_REPLACEMENT} ${NUM_CORE}
```
# Run simulation

Execute `run_champsim.sh` with proper input arguments. The default `TRACE_DIR` in `run_champsim.sh` is set to `$PWD/dpc3_traces`. <br>

* Single-core simulation: Run simulation with `run_champsim.sh` script.

```
Usage: ./run_champsim.sh [BINARY] [N_WARM] [N_SIM] [TRACE] [OPTION]
$ ./run_champsim.sh bimodal-no-no-no-next_line-lru-1core 1 10 600.perlbench_s-210B.champsimtrace.xz

${BINARY}: ChampSim binary compiled by "build_champsim.sh" (bimodal-no-no-no-next_line-lru-1core)
${N_WARM}: number of instructions for warmup (1 million)
${N_SIM}:  number of instructinos for detailed simulation (10 million)
${TRACE}: trace name (600.perlbench_s-210B.champsimtrace.xz)
${OPTION}: extra option for "-low_bandwidth" (src/main.cc)
```
Simulation results will be stored under "results_${N_SIM}M" as a form of "${TRACE}-${BINARY}-${OPTION}.txt".<br> 

* Multi-core simulation: Run simulation with `run_4core.sh` script. <br>
```
Usage: ./run_4core.sh [BINARY] [N_WARM] [N_SIM] [N_MIX] [TRACE0] [TRACE1] [TRACE2] [TRACE3] [OPTION]
$ ./run_4core.sh bimodal-no-no-no-next_line-lru-4core 1 10 0 600.perlbench_s-210B.champsimtrace.xz \\
  401.bzip2-38B.champsimtrace.xz 403.gcc-17B.champsimtrace.xz 410.bwaves-945B.champsimtrace.xz
```
Note that we need to specify multiple trace files for `run_4core.sh`. `N_MIX` is used to represent a unique ID for mixed multi-programmed workloads. 
