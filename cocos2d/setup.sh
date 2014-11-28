#!/bin/bash
rm -rf cocos2d-0.6.0 || true
rm -rf pyglet-1.1.4 || true
tar -xf cocos2d-*.tar.lzma
tar -xf pyglet-*.tar.lzma
cat cocos-samples-patch.patch.lzma | lzma -d > cocos-samples-patch.patch

cd cocos2d-*
patch -p1 -i ../cocos-samples-patch.patch

echo "Now go to cocos2d-0.6.0/samples and execute all the samples there. Only samples has been patched"
echo "Be awesome :)"
