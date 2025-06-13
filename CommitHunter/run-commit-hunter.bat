set "GOOD_BUILD=openjdk version "21.0.7-beta" 2025-04-15 IBM Semeru Runtime Open Edition 21.0.7+6-202504292333 Eclipse OpenJ9 VM 21.0.7+6-202504292333 OpenJ9 - ab9584ee40 OMR - 38fbca611 JCL - 39c20bca9"

set "BAD_BUILD=openjdk version "21.0.8-beta" 2025-07-15 IBM Semeru Runtime Open Edition 21.0.8+2-202505132342 Eclipse OpenJ9 VM 21.0.8+2-202505132342 OpenJ9 - 4d92969242 OMR - b4802c56c JCL - 2119fbf3f"

bash commit_hunter.sh "!GOOD_BUILD!" "!BAD_BUILD!"