import numpy as onp

from jaxlie import SE3

#############################
# (1) Constructing transforms.
#############################

# We can compute a w<-b transform by integrating over an se(3) screw, equivalent
# to `SE3.from_matrix(expm(wedge(twist)))`.
twist = onp.array([1.0, 0.0, 0.2, 0.0, 0.5, 0.0])
T_w_b = SE3.exp(twist)

# We can print the (quaternion) rotation term; this is an `SO3` object:
print(T_w_b.rotation())

# Or print the translation; this is a simple array with shape (3,):
print(T_w_b.translation())

# Or the underlying parameters; this is a length-7 (quaternion, translation) array:
print(T_w_b.wxyz_xyz)  # SE3-specific field.
print(T_w_b.parameters())  # Helper shared by all groups.

# There are also other helpers to generate transforms, eg from matrices:
T_w_b = SE3.from_matrix(T_w_b.as_matrix())

# Or from explicit rotation and translation terms:
T_w_b = SE3.from_rotation_and_translation(
    rotation=T_w_b.rotation(),
    translation=T_w_b.translation(),
)

# Or with the dataclass constructor + the underlying length-7 parameterization:
T_w_b = SE3(wxyz_xyz=T_w_b.wxyz_xyz)


#############################
# (2) Applying transforms.
#############################

# Transform points with the `@` operator:
p_b = onp.random.randn(3)
p_w = T_w_b @ p_b
print(p_w)

# or `.apply()`:
p_w = T_w_b.apply(p_b)
print(p_w)

# or the homogeneous matrix form:
p_w = (T_w_b.as_matrix() @ onp.append(p_b, 1.0))[:-1]
print(p_w)


#############################
# (3) Composing transforms.
#############################

# Compose transforms with the `@` operator:
T_b_a = SE3.identity()
T_w_a = T_w_b @ T_b_a
print(T_w_a)

# or `.multiply()`:
T_w_a = T_w_b.multiply(T_b_a)
print(T_w_a)


#############################
# (4) Misc.
#############################

# Compute inverses:
T_b_w = T_w_b.inverse()
identity = T_w_b @ T_b_w
print(identity)

# Compute adjoints:
adjoint_T_w_b = T_w_b.adjoint()
print(adjoint_T_w_b)

# Recover our twist, equivalent to `vee(logm(T_w_b.as_matrix()))`:
recovered_twist = T_w_b.log()
print(recovered_twist)
