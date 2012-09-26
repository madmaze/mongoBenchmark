#!/bin/bash

#out_dump_1_1 ~320 14:28:00 2012
python ./stacked_plots.py --start-time "26-09 14:27:50" --length 340 --output out_dump_1.png ./plot_setup.example

#out_dump_2_* ~160 14:33:30 2012
python ./stacked_plots.py --start-time "26-09 14:33:20" --length 180 --output out_dump_2.png ./plot_setup.example

#out_dump_4_* ~104 14:36:22 2012
python ./stacked_plots.py --start-time "26-09 14:36:12" --length 124 --output out_dump_4.png ./plot_setup.example

#out_dump_8_* ~130 14:38:45 2012
python ./stacked_plots.py --start-time "26-09 14:38:35" --length 150 --output out_dump_8.png ./plot_setup.example

#out_load_1_1 ~613 07:54:00 2012
python ./stacked_plots.py --start-time "26-09 07:44:00" --length 625 --output out_load_1.png ./plot_setup.example

#out_load_2_1 ~533 08:03:00 2012
python ./stacked_plots.py --start-time "26-09 07:54:00" --length 550 --output out_load_2.png ./plot_setup.example

#out_load_4_1 ~604 08:12:00 2012
python ./stacked_plots.py --start-time "26-09 08:03:00" --length 624 --output out_load_4.png ./plot_setup.example

#out_load_8_1 ~600 08:24:00 2012
python ./stacked_plots.py --start-time "26-09 08:12:00" --length 600 --output out_load_8.png ./plot_setup.example

#out_load_unsharded_1_1 ~600 15:33:00 2012
python ./stacked_plots.py --start-time "26-09 15:22:00" --length 660 --output out_load_unsharded_1.png ./plot_setup.example

#out_load_unsharded_2_* ~705 15:44:00 2012
python ./stacked_plots.py --start-time "26-09 15:33:00" --length 725 --output out_load_unsharded_2.png ./plot_setup.example

#out_load_unsharded_4_* ~705 15:59:00 2012
python ./stacked_plots.py --start-time "26-09 15:44:00" --length 725 --output out_load_unsharded_4.png ./plot_setup.example

#out_load_unsharded_8_* ~816 16:15:00 2012
python ./stacked_plots.py --start-time "26-09 16:00:00" --length 836 --output out_load_unsharded_8.png ./plot_setup.example
