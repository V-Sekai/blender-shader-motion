# Readme

The `ShaderMotion.blend` file has an already set up avatar decoding motion from the
included video clip (Limbo.mp4, a dancing clip from the ShaderMotion webgl demo).

The avatar is the CC0 female base from VRM since it has no redistribution issues.

If you want to use your own avatar though, you'll need to read this to do it.

First get ShaderMotion from the repo and extract it into Assets/ShaderMotion in
Unity as you would usually do. At time of writing latest is v1.9.5 at 229ccbf6,
but the latest version will probably be OK also.

https://gitlab.com/lox9973/ShaderMotion/-/releases/v1.9.5
https://gitlab.com/lox9973/ShaderMotion/-/commit/229ccbf6b75ff0d49a46ca381f587ea8dece05da

Then, replace the file `Assets/ShaderMotion/Script/Common/MeshPlayerGen.cs` with the one
included. It contains a few extra lines that dumps all of the mesh data into a txt file
when playing a Mesh Player.

With your avatar ready in Blender, apply rotation and scale on all meshes, export it to FBX and import it in Unity as you
normally would. I recommend setting:
- 'Apply Scalings' to `FBX All`.
- Keeping 'Forward' as `-Z Forward`.
- Keeping 'Up' as `Y Up`.
- Disabling 'Apply Unit'
- Disabling adding leaf bones, but it doesn't really matter

Then do your Humanoid setup in Unity as usual.

Then, drag the avatar into a scene and on the Animator click the three dots in the top
right and press 'CreateMeshPlayer'. This might take a little longer than usual since
it's dumping the mesh data also.

In the same folder as your FBX, a folder will be made called `auto` that contains the
mesh player meshes. With the patch, it will also contain a plaintext dump of the mesh
data, including the relevant ShaderMotion UVs.

Back in Blender, **ensure you have your system console window toggled on!**.
Otherwise blender might just look frozen for a long time

Open `blender_uvs_from_dump.py` in the Blender scripting workspace. Change the path to
point to the `.mesh.dump.txt` created when you did MeshPlayer creation. When you run it,
it'll perform an absolutely terrible method of matching your Unity verts to Blender ones.
It's not very good at it, and it will take a while, which is why you should have your
system console open to see its progress.

You should make sure your OBJECT names match the Unity mesh names. With the Blender FBX
exporter, this is usually the case by default.

In the system console, you'll see it doing this matching. It shows progress at the start
of the line, which mesh it's doing it on, the vert coord, and the amount of matches at the
end. It should show 1 at the end in the best case, never 0, and may show more if you have
intersecting vertices. The mesh dump does include normals and whatnot as well and you're
welcome to make a better implementation if you feel like it. It was good enough for me.

At this point, all of your affected meshes will have gained a ShaderMotion and ShaderMotion2
UV layer. Unity allows a UV map to have 4 dimensions. In Blender, it's only two. Hence
there being two in Blender.

You can apply the ShaderMotion geo nodes modifier to all meshes, use the spreadsheet button
on the UVs inputs to select an attribute, and select the ShaderMotion and ShaderMotion2
attributes as the UVs. This should happen by default, but if it doesn't, that's how you do it.

Max bone depth should pretty much always be 16. If lowering it doesn't change anything
on your avatar, you can do it, but it's 16 in the actual ShaderMotion shader.

To get the Bone texture, drop the `TextureExport.cs` somewhere in your project.
In the `auto` folder as before, there should be one mesh with a right arrow rollout.
If you roll it out, you'll see the Bone and Shape textures.
With the script, you can select one of these textures, and pressing the cog in the
top right of the inspector, 'Export to EXR'.
Unity won't realize anything has happened but if you refocus the window or look in
Explorer you'll see it's made an `.exr` by the same name as the mesh.

To import it into Blender, use the image view in the bottom left of the Shading workspace.
After opening the image, press N to open the sidepanel and in the 'Image' panel
ensure you set 'Color Space' to 'Non Color'.

You can also use this view to import your video source, also set its Color Space to
'Non Color' and then press the little refresh button on the Frames input to ensure
the entire footage is available.

Now you can return to the modifiers and set Bone, and Image as your video source.
You will need to either keyframe or use a driver to set the correct Frame that you
want the pose to read from.

The Frame input is a float. The modifier will automatically interpolate between
frames if this is given a non-integer value!! So you can render at 60fps when
playing back from 30fps ShaderMotion footage, but you will need to key the frame
value to match the source footage.

The Layer represents the same thing it does in regular ShaderMotion - which
'actor' to play back.

The performance of the modifier will not knock your socks off, it's pretty slow.
But you can still render with it and it's a complete impl other than _Shape
deformation.

You shouldn't use the original Armature to pose once you have the modifier on,
unless you want things to explode. You CAN actually use shape keys or
displacement though, if that's what you want to do.
