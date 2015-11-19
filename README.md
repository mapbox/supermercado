# supermercado
## Supercharger for mercantile

`supermercado` extends the functionality of `mercantile` with additional powerful (though more dependency heavy) commands

## Commands

`supermercado edges`

```
  TILES       ------------     EDGETILES
[x, y, z]     supermercado     [x, y, z]
...       ==>    edges     ==> ...
[x, y, z]     ------------     [x, y, z] 
```

![image](https://cloud.githubusercontent.com/assets/5084513/11233655/fa2b102c-8d74-11e5-96f4-ae1194c9120d.png)

`supermercado union`

```
  TILES       ------------      GEOJSON
[x, y, z]     supermercado      Feature
...       ==>    union     ==> collection
[x, y, z]     ------------     of shape
```

+ all the other mercantile commands you've come to know and love
