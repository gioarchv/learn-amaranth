/* Automatically generated by nMigen 0.2.dev74+g6c5afdc. Do not edit. */
/* Generated by Yosys 0.9 (git sha1 1979e0b) */

(* generator = "nMigen" *)
(* \nmigen.hierarchy  = "top.cd_sync" *)
module cd_sync(clk, clk100_0__i, rst_0__i, rst);
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:367" *)
  wire \$1 ;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:367" *)
  wire \$3 ;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:370" *)
  wire [11:0] \$5 ;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:370" *)
  wire [11:0] \$6 ;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:373" *)
  output clk;
  reg clk;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:137" *)
  input clk100_0__i;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:362" *)
  reg por_clk;
  (* init = 1'h0 *)
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:365" *)
  reg reset_sync_ready = 1'h0;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:365" *)
  reg \reset_sync_ready$next ;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:373" *)
  output rst;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:137" *)
  input rst_0__i;
  (* init = 11'h000 *)
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:364" *)
  reg [10:0] timer = 11'h000;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:364" *)
  reg [10:0] \timer$next ;
  assign \$1  = timer == (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:367" *) 11'h5dc;
  assign \$3  = timer == (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:367" *) 11'h5dc;
  assign \$6  = timer + (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:370" *) 1'h1;
  always @(posedge por_clk)
      timer <= \timer$next ;
  always @(posedge por_clk)
      reset_sync_ready <= \reset_sync_ready$next ;
  reset_sync reset_sync (
    .clk(clk),
    .ready(reset_sync_ready),
    .rst(rst),
    .rst_0__i(rst_0__i)
  );
  always @* begin
    por_clk = 1'h0;
    por_clk = clk100_0__i;
  end
  always @* begin
    \reset_sync_ready$next  = reset_sync_ready;
    (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:367" *)
    casez (\$1 )
      /* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:367" */
      1'h1:
          \reset_sync_ready$next  = 1'h1;
    endcase
  end
  always @* begin
    \timer$next  = timer;
    (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:367" *)
    casez (\$3 )
      /* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:367" */
      1'h1:
          /* empty */;
      /* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:369" */
      default:
          \timer$next  = \$5 [10:0];
    endcase
  end
  always @* begin
    clk = 1'h0;
    clk = clk100_0__i;
  end
  assign \$5  = \$6 ;
endmodule

(* generator = "nMigen" *)
(* \nmigen.hierarchy  = "top.pin_clk100_0" *)
module pin_clk100_0(clk100_0__io, clk100_0__i);
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:137" *)
  output clk100_0__i;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:129" *)
  inout clk100_0__io;
  SB_GB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h01)
  ) clk100_0_0 (
    .GLOBAL_BUFFER_OUTPUT(clk100_0__i),
    .PACKAGE_PIN(clk100_0__io)
  );
endmodule

(* generator = "nMigen" *)
(* \nmigen.hierarchy  = "top.pin_led_0" *)
module pin_led_0(led_0__io, led_0__o);
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:129" *)
  inout [7:0] led_0__io;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:137" *)
  input [7:0] led_0__o;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) led_0_0 (
    .D_OUT_0(led_0__o[0]),
    .PACKAGE_PIN(led_0__io[0])
  );
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) led_0_1 (
    .D_OUT_0(led_0__o[1]),
    .PACKAGE_PIN(led_0__io[1])
  );
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) led_0_2 (
    .D_OUT_0(led_0__o[2]),
    .PACKAGE_PIN(led_0__io[2])
  );
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) led_0_3 (
    .D_OUT_0(led_0__o[3]),
    .PACKAGE_PIN(led_0__io[3])
  );
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) led_0_4 (
    .D_OUT_0(led_0__o[4]),
    .PACKAGE_PIN(led_0__io[4])
  );
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) led_0_5 (
    .D_OUT_0(led_0__o[5]),
    .PACKAGE_PIN(led_0__io[5])
  );
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) led_0_6 (
    .D_OUT_0(led_0__o[6]),
    .PACKAGE_PIN(led_0__io[6])
  );
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) led_0_7 (
    .D_OUT_0(led_0__o[7]),
    .PACKAGE_PIN(led_0__io[7])
  );
endmodule

(* generator = "nMigen" *)
(* \nmigen.hierarchy  = "top.pin_rst_0" *)
module pin_rst_0(rst_0__io, rst_0__i);
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:416" *)
  wire \$1 ;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:137" *)
  output rst_0__i;
  reg rst_0__i;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:415" *)
  wire rst_0__i_n;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:129" *)
  inout rst_0__io;
  assign \$1  = ~ (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:416" *) rst_0__i_n;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h01)
  ) rst_0_0 (
    .D_IN_0(rst_0__i_n),
    .PACKAGE_PIN(rst_0__io)
  );
  always @* begin
    rst_0__i = 1'h0;
    rst_0__i = \$1 ;
  end
endmodule

(* generator = "nMigen" *)
(* \nmigen.hierarchy  = "top.cd_sync.reset_sync" *)
module reset_sync(clk, ready, rst_0__i, rst);
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:376" *)
  wire \$1 ;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:376" *)
  wire \$3 ;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/lib/cdc.py:147" *)
  reg async_ff_clk;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/lib/cdc.py:147" *)
  reg async_ff_rst;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:373" *)
  input clk;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:365" *)
  input ready;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:373" *)
  output rst;
  reg rst;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:137" *)
  input rst_0__i;
  (* init = 1'h1 *)
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/lib/cdc.py:148" *)
  reg stage0 = 1'h1;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/lib/cdc.py:148" *)
  reg \stage0$next ;
  (* init = 1'h1 *)
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/lib/cdc.py:148" *)
  reg stage1 = 1'h1;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/lib/cdc.py:148" *)
  reg \stage1$next ;
  assign \$1  = ~ (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:376" *) ready;
  assign \$3  = \$1  | (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:376" *) rst_0__i;
  always @(posedge async_ff_clk or posedge async_ff_rst)
    if (async_ff_rst)
      stage1 <= 1'h1;
    else
      stage1 <= \stage1$next ;
  always @(posedge async_ff_clk or posedge async_ff_rst)
    if (async_ff_rst)
      stage0 <= 1'h1;
    else
      stage0 <= \stage0$next ;
  always @* begin
    \stage0$next  = stage0;
    \stage0$next  = 1'h0;
  end
  always @* begin
    \stage1$next  = stage1;
    \stage1$next  = stage0;
  end
  always @* begin
    async_ff_rst = 1'h0;
    async_ff_rst = \$3 ;
  end
  always @* begin
    async_ff_clk = 1'h0;
    async_ff_clk = clk;
  end
  always @* begin
    rst = 1'h0;
    rst = stage1;
  end
endmodule

(* generator = "nMigen" *)
(* top =  1  *)
(* \nmigen.hierarchy  = "top" *)
module top(clk100_0__io, rst_0__io, led_0__io);
  (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:58" *)
  wire \$1 ;
  (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:59" *)
  wire [7:0] \$3 ;
  (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:58" *)
  wire \$5 ;
  (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:62" *)
  wire [26:0] \$7 ;
  (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:62" *)
  wire [26:0] \$8 ;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:137" *)
  wire cd_sync_clk100_0__i;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:137" *)
  wire cd_sync_rst_0__i;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:373" *)
  wire clk;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:129" *)
  inout clk100_0__io;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:129" *)
  inout [7:0] led_0__io;
  (* init = 8'h00 *)
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:137" *)
  reg [7:0] pin_led_0_led_0__o = 8'h00;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:137" *)
  reg [7:0] \pin_led_0_led_0__o$next ;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/vendor/lattice_ice40.py:373" *)
  wire rst;
  (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/build/res.py:129" *)
  inout rst_0__io;
  (* init = 26'h0000000 *)
  (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:56" *)
  reg [25:0] timer = 26'h0000000;
  (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:56" *)
  reg [25:0] \timer$next ;
  assign \$1  = timer == (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:58" *) 26'h2faf080;
  assign \$3  = ~ (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:59" *) pin_led_0_led_0__o;
  assign \$5  = timer == (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:58" *) 26'h2faf080;
  assign \$8  = timer + (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:62" *) 1'h1;
  always @(posedge clk)
      timer <= \timer$next ;
  always @(posedge clk)
      pin_led_0_led_0__o <= \pin_led_0_led_0__o$next ;
  cd_sync cd_sync (
    .clk(clk),
    .clk100_0__i(cd_sync_clk100_0__i),
    .rst(rst),
    .rst_0__i(cd_sync_rst_0__i)
  );
  pin_clk100_0 pin_clk100_0 (
    .clk100_0__i(cd_sync_clk100_0__i),
    .clk100_0__io(clk100_0__io)
  );
  pin_led_0 pin_led_0 (
    .led_0__io(led_0__io),
    .led_0__o(pin_led_0_led_0__o)
  );
  pin_rst_0 pin_rst_0 (
    .rst_0__i(cd_sync_rst_0__i),
    .rst_0__io(rst_0__io)
  );
  always @* begin
    \pin_led_0_led_0__o$next  = pin_led_0_led_0__o;
    (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:58" *)
    casez (\$1 )
      /* src = "/home/parallels/github/learn-nMigen/blink/blink.py:58" */
      1'h1:
          \pin_led_0_led_0__o$next  = \$3 ;
    endcase
    (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/hdl/xfrm.py:530" *)
    casez (rst)
      1'h1:
          \pin_led_0_led_0__o$next  = 8'h00;
    endcase
  end
  always @* begin
    \timer$next  = timer;
    (* src = "/home/parallels/github/learn-nMigen/blink/blink.py:58" *)
    casez (\$5 )
      /* src = "/home/parallels/github/learn-nMigen/blink/blink.py:58" */
      1'h1:
          \timer$next  = 26'h0000000;
      /* src = "/home/parallels/github/learn-nMigen/blink/blink.py:61" */
      default:
          \timer$next  = \$7 [25:0];
    endcase
    (* src = "/home/parallels/.local/lib/python3.10/site-packages/nmigen/hdl/xfrm.py:530" *)
    casez (rst)
      1'h1:
          \timer$next  = 26'h0000000;
    endcase
  end
  assign \$7  = \$8 ;
endmodule