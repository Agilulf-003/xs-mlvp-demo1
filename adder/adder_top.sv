module adder_top;

  logic [3:0] a_i;
  logic [3:0] b_i;
  logic [4:0] sum_o;


 adder adder(
    .a_i(a_i),
    .b_i(b_i),
    .sum_o(sum_o)
 );


  export "DPI-C" function get_a_ixxEdQpS5xUWuW;
  export "DPI-C" function set_a_ixxEdQpS5xUWuW;
  export "DPI-C" function get_b_ixxEdQpS5xUWuW;
  export "DPI-C" function set_b_ixxEdQpS5xUWuW;
  export "DPI-C" function get_sum_oxxEdQpS5xUWuW;


  function void get_a_ixxEdQpS5xUWuW;
    output logic [3:0] value;
    value=a_i;
  endfunction

  function void set_a_ixxEdQpS5xUWuW;
    input logic [3:0] value;
    a_i=value;
  endfunction

  function void get_b_ixxEdQpS5xUWuW;
    output logic [3:0] value;
    value=b_i;
  endfunction

  function void set_b_ixxEdQpS5xUWuW;
    input logic [3:0] value;
    b_i=value;
  endfunction

  function void get_sum_oxxEdQpS5xUWuW;
    output logic [4:0] value;
    value=sum_o;
  endfunction



  initial begin
    $dumpfile("adder.fst");
    $dumpvars(0, adder_top);
  end

  export "DPI-C" function finish_EdQpS5xUWuW;
  function void finish_EdQpS5xUWuW;
    $finish;
  endfunction


endmodule
