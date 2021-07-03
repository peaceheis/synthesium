import moderngl
import moderngl_window as mglw

ctx = moderngl.create_standalone_context(require=410)


prog = ctx.program(
    vertex_shader='''
        #version 410

        in vec2 in_vert;
        in vec3 in_color;

        out vec3 v_color;

        void main() {
            v_color = in_color;
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }
    ''',
    fragment_shader='''
        #version 410

        in vec3 v_color;

        out vec3 f_color;

        void main() {
            f_color = v_color;
        }
    ''',
)

class Test(mglw.WindowConfig):
    gl_version = (3, 3)

    def render(self, time, frametime):
        self.ctx.clear(1.0, 0.0, 0.0, 0.0)
    

Test.run()