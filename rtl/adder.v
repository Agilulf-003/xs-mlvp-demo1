module #(
    parameter WIDTH = 4
) adder (
    input [WIDTH-1:0] a_i,
    input [WIDTH-1:0] b_i,
    input [WIDTH:0] sum_o
);
assign sum_o = a_i+b_i;
endmodule
