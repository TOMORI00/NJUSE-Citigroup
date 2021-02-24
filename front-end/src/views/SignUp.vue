2021/2/23 mjh
注册页面

<template>
  <div>
    <BackGround></BackGround>
    <Heading_1></Heading_1>
    <el-container>
      <el-main class="input-form">
        <el-form :model="signUpDataForm" :rules="signUpData" ref="signUpDataForm" class="signup-input">
          <el-form-item prop="name">
            <el-input v-model="signUpDataForm.name" placeholder="用户名"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="signUpDataForm.pwd" placeholder="密码" show-password></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="signUpDataForm.pwdAck" placeholder="确认密码" show-password></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type='primary' @click="ackSignUp('signUpDataForm')" class="choose-button"
                       style="margin-right: 20px">确认
            </el-button>
            <el-button type='primary' @click="toLogin" class="choose-button" style="margin-left: 20px">取消</el-button>
          </el-form-item>
        </el-form>
      </el-main>
    </el-container>
  </div>
</template>

<script>
    import Heading_1 from "../components/Heading_1";
    import BackGround from "../components/BackGround";

    import Global from "../components/GlobalData";

    import {signUpAPI} from "../api/upload";

    export default {
        name: "SignUp",
        data() {
            return {
                signUpDataForm: {
                    name: '',
                    pwd: '',
                    pwdAck: '',
                },
                signUpData: {
                    name: [
                        {required: true, message: '请输入用户名', trigger: 'blur'}
                    ],
                    pwd: [
                        {required: true, message: '请输入密码', trigger: 'blur'}
                    ],
                    pwdAck: [
                        {required: true, message: '请再次输入密码', trigger: 'blur'}
                    ]
                }
            }
        },
        components: {
            Heading_1,
            BackGround
        },
        methods: {
            // 2021-2-24 mjh
            // 确认注册函数，向后端发送注册信息
            async ackSignUp(signUpDataForm) {
                await this.$refs[signUpDataForm].validate((valid) => {
                    if (valid) {
                        if (this.signUpDataForm.pwd === this.signUpDataForm.pwdAck) {
                            let res = true;
                            // res = signUpAPI({
                            //     name: this.signUpDataForm.name,
                            //     pwd: this.signUpDataForm.pwd,
                            // })
                            if (res) {
                                this.$notify.info({
                                    title: '信息',
                                    message: '注册成功',
                                })
                                setTimeout((res => {
                                    this.$router.push('/login')
                                }), 3000)
                            } else {
                                this.$notify.error({
                                    title: '错误',
                                    message: '注册失败'
                                });
                            }
                        } else {
                            this.$notify.error({
                                title: '错误',
                                message: '两次输入密码不一致'
                            });
                        }
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            toLogin() {
                this.signUpDataForm.name = ''
                this.signUpDataForm.pwd = ''
                this.signUpDataForm.pwdAck = ''
                this.$router.back();
            },
        },
    }
</script>

<style scoped>
  @import url('../components/GlobalStyle.css');
</style>