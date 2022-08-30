#!/bin/sh

# find a small rig (bimonoidal) category

mace4 -f cat.mace sym_mon_cat.mace monoidal_add_cat.mace laplaza_cat.mace arrow_cat.mace > output.dump


# takes 20 minutes, but it works:
#prover9 -f cat.mace cat_extra.mace sym_mon_cat.mace sym_mon_goal.mace 

