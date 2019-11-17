# PCGMM

## Image Generation
Please use the following code to generate your image map
* Be noted that you need to put the icons of tiles into "/data/pics/" folder

```python
import img_gen as ig

imgs_dic = ig.getAllTileImg("../data/pics")

# m should be a nparray of the room, normally shape(16,9)
ig.showRoom(m,imgs_dic) 
```
