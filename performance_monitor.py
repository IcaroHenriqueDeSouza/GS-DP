from dataclasses import dataclass
import time
import tracemalloc


@dataclass
class ExecutionResult:
    execution_time_ms: float
    memory_mb: float
    calls: int
    result: object


@dataclass
class BenchmarkResult:
    sizes: list[int]
    execution_times: list[float]
    memory_usage: list[float]
    average_time_ms: float
    average_memory_mb: float


def monitor_algorithm(
    algorithm,
    *args,
    calls: int = 0,
    **kwargs
) -> ExecutionResult:
    """
    Executa um algoritmo e mede:
    - Tempo de execução usando time.perf_counter()
    - Pico de memória via tracemalloc
    - Número de chamadas (quando informado)
    """

    tracemalloc.start()

    start_time = time.perf_counter()

    result = algorithm(
        *args,
        **kwargs
    )

    end_time = time.perf_counter()

    _, peak_memory = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    execution_time_ms = (
        end_time - start_time
    ) * 1000

    memory_mb = (
        peak_memory
        / (1024 * 1024)
    )

    return ExecutionResult(
        execution_time_ms=execution_time_ms,
        memory_mb=memory_mb,
        calls=calls,
        result=result
    )


def benchmark_algorithm(
    algorithm,
    scenario_generator,
    sizes: list[int]
) -> BenchmarkResult:
    execution_times = []
    memory_usage = []

    for size in sizes:
        
        scenario = scenario_generator(size)

        total_cells = size * size

        execution = monitor_algorithm(
            algorithm,
            scenario.cost,
            scenario.risk,
            total_cells  
        )

        execution_times.append(
            execution.execution_time_ms
        )

        memory_usage.append(
            execution.memory_mb
        )

    average_time_ms = (
        sum(execution_times) / len(execution_times)
        if execution_times
        else 0.0
    )

    average_memory_mb = (
        sum(memory_usage) / len(memory_usage)
        if memory_usage
        else 0.0
    )

    return BenchmarkResult(
        sizes=sizes,
        execution_times=execution_times,
        memory_usage=memory_usage,
        average_time_ms=average_time_ms,
        average_memory_mb=average_memory_mb
    )


if __name__ == "__main__":
    from scenarios import (
        generate_small_scenario,
        generate_random_scenario
    )
    from dynamic_programming import dp_bottom_up, dp_top_down

    scenario = generate_small_scenario()

    execution_bu = monitor_algorithm(
        dp_bottom_up,
        scenario.cost,
        scenario.risk,
        25
    )

    print("\n=== Execução Única (Bottom-Up) ===")
    print(f"Tempo: {execution_bu.execution_time_ms:.4f} ms")
    print(f"Memória: {execution_bu.memory_mb:.4f} MB")

    execution_td = monitor_algorithm(
        dp_top_down,
        scenario.cost,
        scenario.risk,
        25
    )
    print("\n=== Execução Única (Top-Down com Memoização) ===")
    print(f"Tempo: {execution_td.execution_time_ms:.4f} ms")
    print(f"Memória: {execution_td.memory_mb:.4f} MB")

    sizes_to_test = [3, 5, 10, 20]
    
    benchmark = benchmark_algorithm(
        dp_bottom_up,
        generate_random_scenario,
        sizes_to_test
    )

    print("\n=== Relatório de Benchmark (Bottom-Up) ===")
    print(f"Tamanhos testados: {benchmark.sizes}")
    print(f"Tempos por tamanho (ms): {[round(t, 4) for t in benchmark.execution_times]}")
    print(f"Memória por tamanho (MB): {[round(m, 4) for m in benchmark.memory_usage]}")
    print(f"Média de Tempo: {benchmark.average_time_ms:.4f} ms")
    print(f"Média de Memória: {benchmark.average_memory_mb:.4f} MB")