# 说明

pip install -r ./requirement.txt

下载getdriver https://blog.csdn.net/yinshuilan/article/details/90713084，然后改下代码里的path变量

我这里用的是火狐的getdriver

把需要爬取的api都写在apilist.txt里，然后运行python ./spider.py

正常爬下来的应该是长这样，例 https://www.tensorflow.org/api_docs/python/tf/image/psnr

```yaml
args:
  a: First set of images.
  b: Second set of images.
  max_val: The dynamic range of the images (i.e., the difference between themaximum
    the and minimum allowed values).
  name: Namespace to embed the computation in.
name: tf.image.psnr
returns: The scalar PSNR between a and b. The returned tensor has type tf.float32and
  shape [batch_size, 1].
url: https://www.tensorflow.org/api_docs/python/tf/image/psnr
```

如果是特征明显的应该会直接放到api_trust文件夹里，出现在其他的文件夹说明需要手动进一步提取

P.S. 发现有些api在官网上几乎没给说明，如https://www.tensorflow.org/api_docs/python/tf/debugging/experimental/disable_dump_debug_info，但是目前提取后会被放在api_trust里，可以再加个条件把这些删了（一般这种api也不会使用到）

有些api的说明特别复杂，没法直接生成期望的提取信息 例：https://www.tensorflow.org/api_docs/python/tf/sparse/SparseTensor