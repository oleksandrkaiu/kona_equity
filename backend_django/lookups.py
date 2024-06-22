from django.db.models import Lookup
from django.db.models import Field

print("LOADED")

@Field.register_lookup
class Match(Lookup):
    lookup_name="mmatch"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        params = [" ".join([f"+{p}*" for p in params[0].split(" ")])]
        return "MATCH (%s) AGAINST (%s IN BOOLEAN MODE)" % (lhs, rhs), params
