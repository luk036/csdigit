import timeit

def bench(name, stmt, globals_dict=None, number=50000):
    if globals_dict is None:
        globals_dict = globals()
    t = timeit.timeit(stmt, globals=globals_dict, number=number)
    ns_per_op = t * 1e9 / number
    print(f"  {name:<30} {ns_per_op:>8.1f} ns/op  ({number} iters)")

print("=== CSD Benchmarks (Python) ===")
bench("to_csd(28.5, 10)", "to_csd(28.5, 10)")
bench("to_csd_i(28)", "to_csd_i(28)")
bench("to_csdnnz(28.5, 4)", "to_csdnnz(28.5, 4)")
bench("to_decimal('+00-00.+0')", "to_decimal('+00-00.+0')")
bench("to_decimal_using_pow('+00-00')", "to_decimal_using_pow('+00-00')")
bench("to_csd(0.0, 10) [zero]", "to_csd(0.0, 10)")
bench("to_csd(-28.5, 10) [neg]", "to_csd(-28.5, 10)")
bench("to_csd(0.5, 10) [small]", "to_csd(0.5, 10)")
bench("to_csd(1024.75, 10) [large]", "to_csd(1024.75, 10)")
