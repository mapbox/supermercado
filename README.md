# supermercado

[![Circle CI](https://circleci.com/gh/mapbox/supermercado/tree/master.svg?style=svg&circle-token=a1a00b2b027b3b6d760cf34fc54be9d168565cad)](https://circleci.com/gh/mapbox/supermercado/tree/master)

`supermercado` extends the functionality of `mercantile` with additional powerful (though more dependency heavy) commands

## Commands

### `supermercado edges`

```
cat tests/fixtures/tiles.txt | supermercado edges | mercantile shapes | fio collect
```

Outputs a stream of `[x, y, z]`s representing the edge tiles of an input stream. Edge tile = any tile that is either directly adjacent to a tile that does not exist, or diagonal to an empty tile.

```
  TILES       ------------     EDGETILES
[x, y, z]     supermercado     [x, y, z]
...       ==>    edges     ==> ...
[x, y, z]     ------------     [x, y, z] 
```

![image](https://cloud.githubusercontent.com/assets/5084513/11233655/fa2b102c-8d74-11e5-96f4-ae1194c9120d.png)

### `supermercado union`

```
cat tests/fixtures/tiles.txt | supermercado union | fio collect
```

Outputs a stream of unioned GeoJSON. Like `mercantile shapes` but as an overall footprint instead of individual shapes for each tile.

```
  TILES       ------------      GEOJSON
[x, y, z]     supermercado      Feature
...       ==>    union     ==> collection
[x, y, z]     ------------     of shape
```

+ all the other mercantile commands you've come to know and love
