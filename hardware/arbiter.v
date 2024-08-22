`timescale 1ns / 1ps

module arbiter (
    input  clk,
    rst,
    input  r  [2:0],
    output g  [2:0]
);
  parameter A = 2'b00,  // "A" State
  B = 2'b01,  // "B" State
  C = 2'b10,  // "C" State
  D = 2'b11;  // "D" State

  reg [1:0] current_state, next_state;

  always @(posedge clk, posedge rst) begin
    if (rst) current_state <= A;
    else current_state <= next_state;
  end

  always_latch @* begin
    case (current_state)
      A: begin
        if (r[0]) begin
          next_state = B;
        end else if (r[1]) begin
          next_state = C;
        end else if (r[2]) begin
          next_state = D;
        end
      end
      B: begin
        if (~r[0]) begin
          next_state = A;
        end
      end
      C: begin
        if (~r[1]) begin
          next_state = A;
        end
      end
      D: begin
        if (~r[2]) begin
          next_state = A;
        end
      end
    endcase
  end

  assign g[0] = (current_state == B);
  assign g[1] = (current_state == C);
  assign g[2] = (current_state == D);

endmodule
