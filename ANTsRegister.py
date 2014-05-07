import os
import emissary
import soaplib
from soaplib.core.service import soap, rpc, DefinitionBase
from soaplib.core.model.primitive import String, Integer
from soaplib.core.model.clazz import ClassModel
from soaplib.core.server import wsgi


CMD_STR = "vendors/ANTs-1.9.v4-Linux/bin/antsRegistration -d 2 -r [{Fixed_Image}, {Moving_Image}, 1] -m MeanSquares[{Fixed_Image}, {Moving_Image},1,2,regular,0.3] -t SyN[0.2,3,0] -c [100x50x25,1e-3,10] -s 2x1x0vox -f 4x2x1 -o [{Registered_Image},{Registered_Image}.nii]"

class RegisterResponse(ClassModel):
    """Response object holds the commandline execution response"""
    statuscode = Integer
    command = String
    stdout = String
    stderr = String
    cwd = String

    output_path = String
    registered_image = String
    registered_gz_image = String
    registered_warp_image = String
    registered_inverse_warp_image = String
    registered_generic_affine_matric = String

    def __init__(self, command=None):
        self.command = command
        self.cwd = '.'
        self.statuscode = 0
        self.stdout = ""
        self.stderr = "Error: I'm sorry I cannot do that, Dave!"

def create_response(out):
    if out:
        r = RegisterResponse(' '.join(out.command))
        r.statuscode = out.status_code
        r.stdout = out.std_out
        r.stderr = out.std_err
    return r

class ANTsRegister(DefinitionBase):
    @soap(String, String, String, _returns=RegisterResponse)
    def register(self, fixed_image, moving_image, output_path):
        fixed_img_filename = os.path.basename(os.path.splitext(fixed_image)[0])
        moving_img_filename = os.path.basename(os.path.splitext(moving_image)[0])
        registered_image = os.path.join(output_path,
                            fixed_img_filename+'_'+moving_img_filename)
        command = CMD_STR.format(Fixed_Image=fixed_image, Moving_Image=fixed_image, Registered_Image=registered_image)
        try:
            out = emissary.envoy.run(command)
            r = create_response(out)
            r.output_path = output_path
            r.registered_image = os.path.join(output_path,
                                            registered_image + ".nii")
            r.registered_gz_image = os.path.join(output_path,
                                            registered_image + ".nii.gz")
            r.registered_warp_image = os.path.join(output_path,
                                            registered_image + "Warp.nii.gz")
            r.registered_inverse_warp_image = os.path.join(output_path,
                                            registered_image + "InverseWarp.nii.gz")
            r.registered_generic_affine_matric = os.path.join(output_path,
                                            registered_image + "GenericAffine.mat")
            return r
        except OSError, e:
            pass
            r = RegisterResponse(command)
            r.statuscode = e.errno
            return e.strerror
        return r

soap_app = soaplib.core.Application([ANTsRegister], 'ants', name='ANTsRegister')
application = wsgi.Application(soap_app)

if __name__=='__main__':
    try:
        from wsgiref.simple_server import make_server
        server = make_server(host='0.0.0.0', port=8080, app=application)
        server.serve_forever()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"
