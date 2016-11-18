"""Define the test group classes."""
from __future__ import division, print_function
import numpy

from six import iteritems
from six.moves import range

from openmdao.api import Group


class TestGroupFlat(Group):
    """Test group flat, with only 1 level of hierarchy."""

    def initialize(self):
        self.metadata.declare('num_sub', typ=int, value=2,
                              desc='total number of components')
        self.metadata.declare('num_var', typ=int, value=2,
                              desc='number of output variables per component')
        self.metadata.declare('var_shape', value=(1,),
                              desc='input/output variable shapes')
        self.metadata.declare('connection_type', typ=str, value='explicit',
                              values=['explicit', 'implicit'],
                              desc='how to connect variables')
        self.metadata.declare('Component',
                              desc='Component class to instantiate')
        self.metadata.declare('derivatives', value='matvec',
                              values=['matvec', 'dense', 'sparse-coo'],
                              desc='method of assembling derivatives')

        num_sub = self.metadata['num_sub']
        num_var = self.metadata['num_var']
        Component = self.metadata['Component']
        for isub in range(num_sub):
            kwargs = {
                'num_input': num_var * (num_sub - 1),
                'num_output': num_var,
                'var_shape': self.metadata['var_shape'],
            }
            if self.metadata['connection_type'] == 'explicit':
                self.add_subsystem('comp_%i'%isub, Component(**kwargs))
            elif self.metadata['connection_type'] == 'implicit':
                renames_inputs = {}
                renames_outputs = {}

                index = 0
                for isub2 in range(num_sub):
                    if isub != isub2:
                        for ivar in range(num_var):
                            index2 = isub2 * num_var + ivar
                            old_name = 'input_%i' % index
                            new_name = 'var_%i' % index2
                            renames_inputs[old_name] = new_name
                            index += 1
                    else:
                        for ivar in range(num_var):
                            index2 = isub2 * num_var + ivar
                            old_name = 'output_%i' % ivar
                            new_name = 'var_%i' % index2
                            renames_outputs[old_name] = new_name

                self.add_subsystem('comp_%i'%isub, Component(**kwargs),
                                   renames_inputs=renames_inputs,
                                   renames_outputs=renames_outputs)

        if self.metadata['connection_type'] == 'explicit':
            for isub in range(num_sub):
                index = 0
                for isub2 in range(num_sub):
                    if isub != isub2:
                        for ivar in range(num_var):
                            ip_name = 'comp_%i.input_%i' % (isub, index)
                            op_name = 'comp_%i.output_%i' % (isub2, ivar)
                            self.connect(op_name, ip_name)
                            index += 1
