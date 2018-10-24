from expects import expect, be_none

from spec.helper import describe, it

from receives.helper import current_module


with describe(current_module):
    with it('returns the callers module'):
        # this is shit but mamba does not register the module it
        # module it runs its execution in. Which means current_module
        # never returns anything else then None
        expect(current_module()).to(be_none)
