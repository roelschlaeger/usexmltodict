.. vim:ts=4:sw=4:tw=0:wm=0:et:ft=rst:nowrap

================
Auto Calibration
================

:Author:     Robert Oelschlaeger
:Date:       27 August 2014
:Contact:    roelsch2009@gmail.com

----

.. contents::

----

Auto Calibration Routine
========================

The auto calibration routine is set up to linearize the response from the LVTRx
and calibrate out the zero offset. To do this the two end points of travel are
used.

Here is what we do for auto calibration:

1.  Perform harmonization (allows motor to spin).
2.  Set solenoid current to zero (no axial displacement).
3.  Spin motor at half speed.
4.  Collect position data every four degrees of shaft rotation to populate Table_1.
5.  Calculate the average of Table_1 values.
6.  Set solenoid current to 1 Amp to drive valve to max open.
7.  Collect position data every four degrees of shaft rotation to populate Table_2.
8.  Calculate the average of Table_2 values.
9.  Calculate values for Table_3 (best fit position correction or
    *rom_harmonize_data*) by averaging Table_1 and Table_2 data points.

    ::

        Table_3[N] = (Table_1[N] + Table_2[N]) / 2

    where:
        - N is the table index for successive four degree incremental values
        - The Table_1 average is the zero offset.
        - The difference between Table_1 and Table_2 is a gain scale factor.

Calibration Data Display
========================

Calibration data can be viewed using the RS232 debug port and the
*DisplayHarmonizeData* command selection, as shown below::

    Application: ACCV_BLDC
    Version:     0.2.8.11
    Build:       20131029

                                                   Harmonize
                            Program State           Offset
                        =========================  =========
                        ALL    MTR1    MTR2_AXIAL
                        ------ ------  ----------  --------
    rom_harmonize_data: 0x0000 0x0000    0x0000     0x55fc
                        \_____________________/
                                |
                                0xffff = Unprogrammed
                                0x0000 = Programmed
                                0x0001 = Partly programmed
                                0x0002 = Misprogrammed



    Enter Password: XXXXXXXX

    Select menu
    1 - menu 1: pi_motor1_phase_detector.param
    2 - menu 2: pi_motor1_idc.param
    3 - menu 3: pi_motor1_rate.param
    4 - menu 4: pi_motor2_idc.param
    5 - menu 5: pi_motor2_position.param

    6 - menu 6: Dac Channel Selection

    7 - RESET

    8 - DisplayHarmonizeData

Selecting *DisplayHarmonizeData*:: 

    8
                                                   Harmonize
                            Program State           Offset
                        =========================  =========
                        ALL    MTR1    MTR2_AXIAL
                        ------ ------  ----------  --------
    rom_harmonize_data: 0x0000 0x0000    0x0000     0x55fc
                        \_____________________/
                                |
                                0xffff = Unprogrammed
                                0x0000 = Programmed
                                0x0001 = Partly programmed
                                0x0002 = Misprogrammed


    rom_harmonize_data
    ==================

    cols 00-04:    0.177883    0.181485    0.177263    0.160720    0.140571
    cols 05-09:    0.133563    0.132405    0.129925    0.121168    0.116266
    cols 10-14:    0.120538    0.118764    0.113832    0.115485    0.119059
    cols 15-19:    0.121871    0.131132    0.136865    0.130735    0.128787
    cols 20-24:    0.136824    0.147551    0.137845    0.128611    0.128641
    cols 25-29:    0.129177    0.117638    0.104029    0.100638    0.100562
    cols 30-34:    0.102443    0.097816    0.097554    0.096358    0.095870
    cols 35-39:    0.100202    0.102628    0.104137    0.104253    0.103700
    cols 40-44:    0.111524    0.120846    0.126988    0.134905    0.143437
    cols 45-49:    0.151411    0.155720    0.141928    0.147719    0.158419
    cols 50-54:    0.152653    0.139366    0.128311    0.123504    0.130040
    cols 55-59:    0.141599    0.129480    0.121493    0.124083    0.141158
    cols 60-64:    0.139463    0.152641    0.148078    0.168555    0.168114
    cols 65-69:    0.180351    0.201203    0.207343    0.204250    0.214174
    cols 70-74:    0.216204    0.207271    0.193938    0.189377    0.184602
    cols 75-79:    0.179836    0.173120    0.174890    0.166526    0.172470
    cols 80-84:    0.167293    0.173621    0.179142    0.180672    0.189402
    cols 85-89:    0.193476    0.191980    0.206092    0.199246    0.203260

    Table 1 Average:    0.146729
    Table 2 Average:    0.146500


----

.. note::
    The tabular data displayed above are values collected during a test run
    using the software test bench motor.
