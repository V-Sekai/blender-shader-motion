# Readme

The `ShaderMotion.blend` file has an already set up avatar decoding motion from the included video clip (Limbo.mp4, a dancing clip from the ShaderMotion webgl demo).

The avatar is the CC0 female base from VRM since it has no redistribution issues.

If you want to use your own avatar though, you'll need to read this to do it.

## Unity Setup

### Step 1: Obtain ShaderMotion

First, get ShaderMotion from the repo and extract it into `Assets/ShaderMotion` in Unity as you would usually do. At the time of writing, the latest is v1.9.5 at commit 229ccbf6, but the latest version will probably be OK also.

- [ShaderMotion v1.9.5 Release](https://gitlab.com/lox9973/ShaderMotion/-/releases/v1.9.5)
- [Commit 229ccbf6](https://gitlab.com/lox9973/ShaderMotion/-/commit/229ccbf6b75ff0d49a46ca381f587ea8dece05da)

### Step 2: Replace MeshPlayerGen.cs

Then, replace the file `Assets/ShaderMotion/Script/Common/MeshPlayerGen.cs` with the one included. It contains a few extra lines that dump all of the mesh data into a txt file when playing a Mesh Player.

### Step 3: Prepare and Import Your Avatar

With your avatar ready in Blender, apply rotation and scale on all meshes, export it to FBX, and import it in Unity as you normally would. Recommended settings include:

- 'Apply Scalings' to `FBX All`.
- Keeping 'Forward' as `-Z Forward`.
- Keeping 'Up' as `Y Up`.
- Disabling 'Apply Unit'
- Disabling adding leaf bones, but it doesn't really matter

### Step 4: Humanoid Setup and Mesh Player Creation

Do your Humanoid setup in Unity as usual. Then, drag the avatar into a scene and on the Animator click the three dots in the top right and press 'CreateMeshPlayer'. This might take a little longer than usual since it's dumping the mesh data also.

### Step 5: Access Generated Data

In the same folder as your FBX, a folder will be made called `auto` that contains the mesh player meshes. With the patch, it will also contain a plaintext dump of the mesh data, including the relevant ShaderMotion UVs.

## Blender Setup

### Step 1: Prepare Blender

Back in Blender, **ensure you have your system console window toggled on!** Otherwise, Blender might just look frozen for a long time.

### Step 2: Run Script for UV Mapping

Open `blender_uvs_from_dump.py` in the Blender scripting workspace. Change the path to point to the `.mesh.dump.txt` created when you did MeshPlayer creation. When you run it, it'll perform an absolutely terrible method of matching your Unity verts to Blender ones. It's not very good at it, and it will take a while, which is why you should have your system console open to see its progress.

### Step 3: Verify Object Names and Matching Process

You should make sure your OBJECT names match the Unity mesh names. With the Blender FBX exporter, this is usually the case by default.

### Step 4: Apply ShaderMotion UV Layers

At this point, all of your affected meshes will have gained a ShaderMotion and ShaderMotion2 UV layer. You can apply the ShaderMotion geo nodes modifier to all meshes, use the spreadsheet button on the UVs inputs to select an attribute, and select the ShaderMotion and ShaderMotion2 attributes as the UVs.

### Step 5: Export and Import Textures

To get the Bone texture, drop the `TextureExport.cs` somewhere in your project. In the `auto` folder as before, there should be one mesh with a right arrow rollout. If you roll it out, you'll see the Bone and Shape textures. With the script, you can select one of these textures, and pressing the cog in the top right of the inspector, 'Export to EXR'. Unity won't realize anything has happened but if you refocus the window or look in Explorer you'll see it's made an `.exr` by the same name as the mesh.

### Step 6: Set Up Shading Workspace

To import it into Blender, use the image view in the bottom left of the Shading workspace. After opening the image, press N to open the side panel and in the 'Image' panel ensure you set 'Color Space' to 'Non Color'.

### Step 7: Configure Modifiers and Playback

Now you can return to the modifiers and set Bone, and Image as your video source. You will need to either keyframe or use a driver to set the correct Frame that you want the pose to read from. The Frame input is a float. The modifier will automatically interpolate between frames if this is given a non-integer value!

### Step 8: Final Adjustments and Rendering

Adjust the Layer to represent the same thing it does in regular ShaderMotion - which 'actor' to play back. Note that the performance of the modifier is quite slow, but it is functional for rendering. Avoid using the original Armature to pose once you have the modifier on, unless you want things to explode. You CAN actually use shape keys or displacement though, if that's what you want to do.
