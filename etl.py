import psycopg2
import pygrametl
from pygrametl.tables import CachedDimension


"""
import luigi
class TransformGrades(luigi.Task):
    def requires(self):
        return ExtractGrades()

    def output(self):
        return PSQLTarget()

    def run(self):
        with self.output().open() as f:

"""

# The actual database connection is handled using a PEP 249 connection
pgconn = psycopg2.connect("""dbname='DwColegio' user='federico'""")

# This ConnectionWrapper will be set as default and is then implicitly used.
# A reference to the wrapper is saved to allow for easy access of it later
conn = pygrametl.ConnectionWrapper(connection=pgconn)

dim_fecha = CachedDimension(
    name='DimFecha',
    key='id',
    attributes=['semestre', 'ano'],
    lookupatts=['semestre', 'ano'],
    prefill=True)

dim_colegio = CachedDimension(
    name='DimColegio',
    key='id',
    attributes=['nombre', 'financiamiento'],
    lookupatts=['semestre', 'ano'],
    prefill=True)

#create fecha table
def duprange(f,l):
    for i in range(f,l):
        yield i
        yield i

"""
semesters = [x for i in range(0,100) for x in range(1,3)]
years = [x for x in duprange (1970, 1970 + 100)]

for i, semester in enumerate(semesters):
   dim_fecha.insert({"semestre":semester, "ano": years[i]})
"""
fecha_id = dim_fecha.lookup({"foo":1, "bar":2010}, {"semestre":"foo", "ano":"bar"})
colegio_id

# if table.lookup(...) is None:
# id = table.insert(...)

conn.commit()
