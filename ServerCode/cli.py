from bubbleScan.repository.memrepo import MemRepo
from bubbleScan.use_cases.scantron_list import scantron_list_use_case

repo = MemRepo([])
result = scantron_list_use_case(repo)

print(result)