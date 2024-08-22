`timescale 1ns / 1ps

module arbiter (
    input  r[2:0],
    output g[2:0]
);
  parameter A = 2'b00,  // "A" State
  B = 2'b01,  // "B" State
  C = 2'b10,  // "C" State
  D = 2'b11;  // "D" State

  reg [1:0] state = A;

  always @* begin
    if (state == A && r[0]) begin
      state = B;
    end else if (state == A && r[1]) begin
      state = C;
    end else if (state == A && r[2]) begin
      state = D;

    end else if (state == B && ~r[0]) begin
      state = A;
    end else if (state == C && ~r[1]) begin
      state = A;
    end else if (state == D && ~r[2]) begin
      state = A;
    end

  end

endmodule
