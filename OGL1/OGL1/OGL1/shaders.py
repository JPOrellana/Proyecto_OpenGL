vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 uvs;

void main()
{
	vec4 newPos = vec4(position.x, position.y + sin(time)/4, position.z, 1.0);

	gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(newPos);
	uvs = texCoords;
}
'''


fragment_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 uvs;

out vec4 fragmentColor;

void main()
{
	fragmentColor = texture(tex, uvs);
}
'''

general_vertex_shader = '''
#version 450 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 uvs;

void main()
{
    vec4 newPos = vec4(position.x, position.y + sin(time) / 4.0, position.z, 1.0);

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(newPos);
    uvs = texCoords;
}
'''

# --------------------------------------------- Shader 1: Arcoiris -------------------------------------------
rainbow_fragment_shader = '''
#version 450 core

uniform float time;  // Declarar la variable "time" en el fragment shader

in vec2 uvs;
out vec4 fragmentColor;

void main()
{
    // Resto del shader que utiliza la variable "time"
    vec3 rainbowColor = vec3(
        0.5 * (1.0 + sin(uvs.x * 3.14159265 * 2.0 + time)),
        0.5 * (1.0 + sin(uvs.x * 3.14159265 * 2.0 + time + 2.094)),
        0.5 * (1.0 + sin(uvs.x * 3.14159265 * 2.0 + time + 4.188))
    );

    fragmentColor = vec4(rainbowColor, 1.0);
}
'''
# --------------------------------------------------------------------------------------------------------------


# ------------------------------------------- Shader 2: Cuadrícula -------------------------------------------
grid_fragment_shader = '''
#version 450 core
in vec2 uvs;
out vec4 fragmentColor;

void main()
{
    int gridSize = 30;  
    vec2 gridUV = floor(uvs * float(gridSize));
    
    float lineThickness = 0.1;  

    float horizontalLine = step(mod(uvs.y * gridSize, 1.0), lineThickness);
    float verticalLine = step(mod(uvs.x * gridSize, 1.0), lineThickness);

    if (mod(int(gridUV.x) + int(gridUV.y), 2) == 0) {
        fragmentColor = vec4(0.255, 0.157, 0.031, 1.0);  
    } else {
        fragmentColor = vec4(0.097, 0.179, 0.033, 1.0);  
    }

    if (horizontalLine > 0.0 || verticalLine > 0.0) {
        fragmentColor = vec4(0.0, 0.0, 0.0, 1.0);  
    }
}

'''
# ------------------------------------------------------------------------------------------------------------


# --------------------------------------------- Shader 3: Ondas/Olas -----------------------------------------
waves_fragment_shader = '''
#version 450 core

uniform float time;
uniform sampler2D tex;  // Agrega una textura

in vec2 uvs;
out vec4 fragmentColor;

void main()
{
    float frequency = 2.0;
    float speed = 0.1;
    vec2 offset = vec2(sin(time * speed), cos(time * speed));
    vec2 disturbedUV = uvs + offset * sin(uvs.x * frequency);
    vec3 waterColor = vec3(0.006, 0.112, 0.231);
    fragmentColor = vec4(mix(waterColor, texture(tex, disturbedUV).xyz, 0.7), 1.0); 
}


'''
# -----------------------------------------------------------------------------------------------------------

# ------------------------------------------- Shader 4: Combinación -----------------------------------------
discoBall_fragment_shader = '''
#version 450 core

uniform float time;
uniform sampler2D tex;

in vec2 uvs;
out vec4 fragmentColor;

void main()
{
    int gridSize = 30;  
    vec2 gridUV = floor(uvs * float(gridSize));
    
    float lineThickness = 0.1;  

    float horizontalLine = step(mod(uvs.y * gridSize, 1.0), lineThickness);
    float verticalLine = step(mod(uvs.x * gridSize, 1.0), lineThickness);

    vec3 rainbowColor = vec3(
        0.5 * (1.0 + sin(uvs.x * 3.14159265 * 2.0 + time)),
        0.5 * (1.0 + sin(uvs.x * 3.14159265 * 2.0 + time + 2.094)),
        0.5 * (1.0 + sin(uvs.x * 3.14159265 * 2.0 + time + 4.188))
    );

    if (mod(int(gridUV.x) + int(gridUV.y), 2) == 0) {
        fragmentColor = vec4(rainbowColor, 1.0);  
    } else {
        fragmentColor = vec4(rainbowColor * 0.5, 1.0);  
    }

    if (horizontalLine > 0.0 || verticalLine > 0.0) {
        fragmentColor = vec4(0.0, 0.0, 0.0, 1.0);  
    }
}

'''
# -----------------------------------------------------------------------------------------------------------

# ------------------------------------------ Shader 6: Dalmata -------------------------------------------
dalmata_fragment_shader = '''
#version 450 core

in vec2 uvs;
out vec4 fragmentColor;

vec2 random(vec2 st) {
    st = vec2(dot(st, vec2(127.1, 311.7)), dot(st, vec2(269.5, 183.3)));
    return -1.0 + 2.0 * fract(sin(st) * 43758.5453123);
}

float noise(vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(mix(dot(random(i + vec2(0.0, 0.0)), f - vec2(0.0, 0.0)),
                   dot(random(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0)), u.x),
               mix(dot(random(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0)),
                   dot(random(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0)), u.x), u.y);
}

void main() {
    float n = noise(uvs * 10.0);

    vec3 paperColor = vec3(0.9, 0.85, 0.8);

    vec3 color = paperColor - n * 10;

    fragmentColor = vec4(color, 1.0);
}


'''
# ----------------------------------------------------------------------------------------------------------