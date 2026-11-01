
module csd_mult_72 (
    input signed [10:0] x,      // Input value
    output signed [16:0] result // Result of multiplication
);

    // Create shifted versions of input
    wire signed [16:0] x_shift6 = x <<< 6;
    wire signed [16:0] x_shift3 = x <<< 3;

    // CSD implementation
    assign result = x_shift6 + x_shift3;
endmodule


module csd_mult_134 (
    input signed [10:0] x,      // Input value
    output signed [17:0] result // Result of multiplication
);

    // Create shifted versions of input
    wire signed [17:0] x_shift7 = x <<< 7;
    wire signed [17:0] x_shift3 = x <<< 3;
    wire signed [17:0] x_shift1 = x <<< 1;

    // CSD implementation
    assign result = x_shift7 + x_shift3 - x_shift1;
endmodule


module csd_mult_194 (
    input signed [10:0] x,      // Input value
    output signed [18:0] result // Result of multiplication
);

    // Create shifted versions of input
    wire signed [18:0] x_shift8 = x <<< 8;
    wire signed [18:0] x_shift6 = x <<< 6;
    wire signed [18:0] x_shift1 = x <<< 1;

    // CSD implementation
    assign result = x_shift8 - x_shift6 + x_shift1;
endmodule


module csd_mult_224 (
    input signed [10:0] x,      // Input value
    output signed [18:0] result // Result of multiplication
);

    // Create shifted versions of input
    wire signed [18:0] x_shift8 = x <<< 8;
    wire signed [18:0] x_shift5 = x <<< 5;

    // CSD implementation
    assign result = x_shift8 - x_shift5;
endmodule

module gaussian_blur_1d (
    input  [7:0] x0, x1, x2, x3, x4, x5, x6,
    output [7:0] y
);
    wire signed [10:0] s3 = x0 + x6;
    wire signed [10:0] s2 = x1 + x5;
    wire signed [10:0] s1 = x2 + x4;
    wire signed [10:0] s0 = x3;

    wire signed [16:0] p3_raw;
    wire signed [17:0] p2_raw;
    wire signed [18:0] p1_raw;
    wire signed [18:0] p0_raw;

    csd_mult_72 m3 (.x(s3), .result(p3_raw));
    csd_mult_134 m2 (.x(s2), .result(p2_raw));
    csd_mult_194 m1 (.x(s1), .result(p1_raw));
    csd_mult_224 m0 (.x(s0), .result(p0_raw));

    wire signed [18:0] p3 = p3_raw;
    wire signed [18:0] p2 = p2_raw;
    wire signed [18:0] p1 = p1_raw;
    wire signed [18:0] p0 = p0_raw;
    wire signed [18:0] total = p3 + p2 + p1 + p0;
    wire signed [18:0] rounded = (total + 19'sd512) >>> 10;

    assign y = rounded[7:0];
endmodule
