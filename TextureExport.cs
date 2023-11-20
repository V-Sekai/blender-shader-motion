// Use this to export internal Texture2Ds out to EXR
// By unrolling the generated mesh from ShaderMotion's MeshPlayerGen, you can select the Bone and Shape textures
// Export them out to EXR and bind them in the relevant playback models.
// _Shape is probably unnecessary if you're not driving blend shapes with any channels

#if UNITY_EDITOR

using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEditor;

namespace Gorialis
{
    public class TextureExport
    {
        [MenuItem("CONTEXT/Texture2D/Export to EXR")]
        static void Export_EXR(MenuCommand command)
        {
            var texture = (Texture2D)command.context;
            var path = AssetDatabase.GetAssetPath(texture);
            Debug.Log(path);
            byte[] bytes = texture.EncodeToEXR(Texture2D.EXRFlags.OutputAsFloat);
            File.WriteAllBytes(path + ".exr", bytes);
        }
    }
}

#endif
