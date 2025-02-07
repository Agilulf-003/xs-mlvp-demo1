module adder_top;

  wire [3:0] a_i;
  wire [3:0] b_i;
  wire [4:0] sum_o;


 adder adder(
    .a_i(a_i),
    .b_i(b_i),
    .sum_o(sum_o)
 );


endmodule
