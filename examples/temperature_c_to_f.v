
module csd_multiplier (
    input signed [7:0] x,      // Input value
    output signed [14:0] result // Result of multiplication
);

    // Create shifted versions of input
    wire signed [14:0] x_shift7 = x <<< 7;
    wire signed [14:0] x_shift4 = x <<< 4;
    wire signed [14:0] x_shift2 = x <<< 2;
    wire signed [14:0] x_shift0 = x <<< 0;

    // CSD implementation
    assign result = x_shift7 - x_shift4 + x_shift2 - x_shift0;
endmodule

module temperature_c_to_f (
    input  signed [7:0] celsius,
    output signed [7:0] fahrenheit
);

    wire signed [14:0] product;
    csd_multiplier mul (.x(celsius), .result(product));

    // 32 * 2**k (the +32 offset) plus 2**(k-1) (round to nearest)
    localparam signed [15:0] OFFSET = 16'sd2080;
    wire signed [15:0] rounded = product + OFFSET;

    assign fahrenheit = rounded >>> 6;
endmodule
