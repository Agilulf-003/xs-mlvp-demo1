//--------------------------
// simple two port adder
//--------------------------

module adder #(
    parameter WIDTH = 4
)(
    input [WIDTH-1:0] a_i,
    input [WIDTH-1:0] b_i,
    output [WIDTH:0] sum_o
);
assign sum_o = a_i+b_i;
endmodule
