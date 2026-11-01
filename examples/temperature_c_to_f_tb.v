
module tb;
    reg signed [7:0] celsius;
    wire signed [7:0] fahrenheit;
    integer i;
    integer expected;
    integer errors;

    temperature_c_to_f dut (.celsius(celsius), .fahrenheit(fahrenheit));

    initial begin
        errors = 0;
        for (i = -9; i <= 30; i = i + 1) begin
            celsius = i;
            #1;
            expected = (18 * i + 325) / 10;
            if (fahrenheit !== expected) begin
                errors = errors + 1;
                $display("MISMATCH c=%0d f=%0d expected=%0d", celsius, fahrenheit, expected);
            end
        end
        if (errors == 0)
            $display("PASS: all 40 readings match round(9/5*C+32)");
        else
            $fatal(1, "FAIL: %0d mismatches", errors);
        $finish;
    end
endmodule
