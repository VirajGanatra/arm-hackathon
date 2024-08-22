`timescale 1ns / 1ps

module test ();
  reg clk;
  reg rst;

  reg [2:0] r;
  wire [2:0] g;

  reg [2:0] before_g, after_g;

  reg ok = 1;
  reg [5:0] vectors[63:0];

  always #1 clk <= ~clk;

  initial begin
    $readmemb("vectors.txt", vectors);
    clk = 0;

    r   = 3'd0;
    #1 rst = 0;
    #1 rst = 1;
    #1 rst = 0;

    for (integer i = 0; i < 8; i = i + 1) begin
      for (integer j = 0; j < 8; j = j + 1) begin
        // Set input
        r = i[2:0];
        #5;

        // $display("Transition from %b to %b:", i[2:0], j[2:0]);
        // $display("Before g = %b", g);
        before_g = g;

        r = j[2:0];
        #5;

        // $display("After g = %b\n", g);
        after_g = g;

        if (before_g != vectors[(i*8)+j][5:3] || after_g != vectors[(i*8)+j][2:0]) begin
          ok = 0;
        end

      end
    end

    if (ok) $display("TEST PASSED");
    else $display("TEST FAILED");

    $finish;
  end

  arbiter a1 (
      clk,
      rst,
      r,
      g
  );
endmodule
