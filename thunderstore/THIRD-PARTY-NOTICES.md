# Third-party notices

Peak Workshop (PeakWorkshop.dll) embeds the following third-party material.

## Unity Unified Ray Tracing compute kernels (`urtkernels.bundle`)

The editor build of Peak Workshop embeds `urtkernels.bundle`, an AssetBundle with nine compute shaders compiled,
unmodified, from the Unity package `com.unity.render-pipelines.core` 17.3.0 (Unity 6000.3.15f1):
`GeometryPoolKernels`, `CopyBuffer`, `CopyPositions`, `bit_histogram`, `block_reduce_part`, `block_scan`,
`build_hlbvh`, `restructure_bvh`, `scatter`. PEAK ships Unity's Unified Ray Tracing runtime without these kernels; Peak
Workshop needs them to bake map lighting on graphics cards without hardware ray tracing (DXR).

> com.unity.render-pipelines.core copyright © 2020 Unity Technologies ApS
>
> Licensed under the Unity Companion License for Unity-dependent projects – see
> [Unity Companion License](https://unity.com/legal/licenses/unity-companion-license).
>
> Unless expressly provided otherwise, the Software under this license is made available strictly on an “AS IS” BASIS
> WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. Please review the license for details on these and other terms and
> conditions.

The bundle was authored with the Unity Editor under a valid Unity engine license and is used only inside PEAK, a game
made with Unity.

### RadeonRays 4.1 (part of the kernels above)

The BVH build kernels are a port of RadeonRays 4.1
(https://github.com/GPUOpen-LibrariesAndSDKs/RadeonRays_SDK), licensed under the MIT License:

> Copyright (c) 2019, 2021 Advanced Micro Devices, Inc. All rights reserved.
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
> documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
> rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
> persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
> Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
> WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
> COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
> OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
