# AttributeToUVMap

Geometory Nodeを適用したモデルはUVMap情報が`属性（Attribute）`に格納されているので、FBXエクスポート時などで反映されない。`属性`を`UVMap`に移動させ、Geometory Node製のモデルのUVを吐き出せるようにするBlenderアドオンです。

Blender 3.0.0以降対応

## 機能

`Face Corner`の`2DVector`形式の`属性`のデータを`UVMap`に移動させることができます。

## 使い方

アドオンをインストール後、`属性`を`UVMap`に移動させたいモデルを選択し`3D Viewport`>`Object`>`Move Attribute to UVMap`>`[移動させたい属性]`を選択します。

