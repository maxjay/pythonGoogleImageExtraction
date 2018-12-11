# pythonGoogleImageExtraction
A python script to harvest batches of images based of terms from Google Images

## How to run
`python main.py -i [search terms] -b [batchSize=100] [-o outputLocation]`

Example:
`python main.py -i dog cat -b 300` will fetch 300 images of 'dog' and 300 images of 'cat'

**To include spaces in term, replace spaces with _ in the input**
Example: `python main.py -i Cats_and_dogs` will fetch 100 images of 'Cats and dogs'

___
