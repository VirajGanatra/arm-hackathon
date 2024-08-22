`timescale 1ns / 1ps

module test ();
  reg clk;
  reg rst;

  reg [2:0] r;
  wire [2:0] g;

  initial begin
    #1 clk = 0;
    r = 3'd0;
    #10 rst = 1;
    #10 rst = 0;

    for (int i = 0; i < 8; i++) begin
      #1 r = i[2:0];
      #1 clk = ~clk;
      #1 clk = ~clk;
      #1 clk = ~clk;
      #1 clk = ~clk;

      $display("r: %b\tg: %b\n", r, g);
    end

    $finish;
  end

  arbiter a1 (
      clk,
      rst,
      r,
      g
  );
endmodule
