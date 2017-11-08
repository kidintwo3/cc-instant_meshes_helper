"""
InstaMesh:

    Copyright (c) 2015 Wenzel Jakob, Daniele Panozzo, Marco Tarini,
    and Olga Sorkine-Hornung. All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its contributors
       may be used to endorse or promote products derived from this software
       without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    You are under no obligation whatsoever to provide any bug fixes, patches, or
    upgrades to the features, functionality or performance of the source code
    ("Enhancements") to anyone; however, if you choose to make your Enhancements
    available either publicly, or directly to the authors of this software, without
    imposing a separate written license agreement for such Enhancements, then you
    hereby grant the following license: a non-exclusive, royalty-free perpetual
    license to install, use, modify, prepare derivative works, incorporate into
    other computer software, distribute, and sublicense such enhancements or
    derivative works thereof, in binary and source code form.

Info:
    InstaMesh helper WIP for Maya

Todo:
    Need to implement QT interface

"""

import subprocess
import tempfile
import os
import maya.cmds as cmds

# Replace this with UI / config file
inst_mesh_path = "c:/Users/janos.hunyadi/Documents/temp/instantmeshes/instant_meshes.exe"


def process_selected(face_count=None):
    if not os.path.exists(inst_mesh_path):
        cmds.warning('Insta Mesh path not found!')
        return

    # Get the current selection
    sel_obj = cmds.ls(sl=True)

    if sel_obj:

        print 'Processing Insta Mesh...'

        # if no polycount set just double the amount of the source object
        if not face_count:
            face_count = int(cmds.polyEvaluate(sel_obj, f=True))
            face_count *= 2

        # Create temp file for OBJ export
        temp = tempfile.NamedTemporaryFile(prefix='instamesh_', suffix='.obj', delete=False)
        temp_path = temp.name

        # Save the currently selected object as an OBJ
        cmds.file(temp_path, force=True, exportSelected=True, type="OBJ")

        # run instamesh command on the OBJ
        some_command = inst_mesh_path + " " + temp_path + " -o " + temp_path + " -f " + str(face_count)
        p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()

        # import back the temp OBJ file
        returnedNodes = cmds.file(temp_path,
                                  i=True,
                                  type="OBJ",
                                  rnn=True,
                                  ignoreVersion=True,
                                  options="mo=0",
                                  loadReferenceDepth="all")
        # delete the temp file
        temp.close()

        # Select the imported nodes
        if returnedNodes:
            cmds.select(returnedNodes, r=True)

        print 'Insta Mesh done...'



    else:
        cmds.warning('No objects selected...')


process_selected()
