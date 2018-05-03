# Redis Module of Spring 2018 Advanced DB Project
## Creating Courses
1. add course number into `courseNums` set
2. splits the course number into dept and number, e.g `csse433` > `csse` and `433`, the course number is then added into the sets `dept:<dept>` and `courseNum:<num>`
3. course name and description are tokenized into words, and the course numbers are added into an index for each word that is 4 letters or more. The indexs look like `ind:<word>`
4. the data is stored into a hashmap with the key `courseOrig:<courseNum>`, this is to help the delete step.
