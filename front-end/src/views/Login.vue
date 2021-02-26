此页为入口页
- 本页元素与交互
- 图片背景
- 左上图标》跳转至某页面
- 上方中央软件名称
- 右上“关于”按钮》跳转至“关于”页面
- 中央登录框
- 输入用户名
- 输入密码
- 点击登录

<template>
    <div>
        <!--        <el-container>-->
        <!--            <el-header class="homepage-header" height="130px">-->
        <!--                <div class="div-logo">-->
        <!--                    <a href="/homepage">-->
        <!--                        <img class="logo-img" src="../assets/nju.png">-->
        <!--                    </a>-->
        <!--                </div>-->
        <!--                <div class="div-more-link">-->
        <!--                    <div class="link-text">-->
        <!--                        <a href="/about"><h2>关于</h2></a>-->
        <!--                    </div>-->
        <!--                </div>-->
        <!--            </el-header>-->

        <!--            <div class="title">公募基金/理财复现与顾问组合系统（EPC）</div>-->
        <BackGround></BackGround>
        <Heading_1></Heading_1>
        <el-container>
            <el-main class="input-form">
                <el-form :model="ruleForm" :rules="rules" ref="ruleForm" class="div-choose">
                    <el-form-item prop="name">
                        <el-input v-model="ruleForm.name" placeholder="用户名"></el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <el-input v-model="ruleForm.password" placeholder="密码" show-password></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type='primary' @click="login('ruleForm')" class="choose-button"
                                   style="margin-right: 20px">登录
                        </el-button>
                        <el-button type='primary' @click="toSignUp" class="choose-button" style="margin-left: 20px">注册
                        </el-button>
                    </el-form-item>
                </el-form>
            </el-main>
        </el-container>

        <!--        </el-container>-->
    </div>
</template>

<script>
import Heading_1 from "../components/Heading_1";
import BackGround from "../components/BackGround";

import Global from "../components/GlobalData";

import {signInAPI} from "../api/upload"

export default {
    name: 'Login',
    data() {
        return {
            ruleForm: {
                name: '',
                password: ''
            },
            rules: {
                name: [
                    {required: true, message: '请输入用户名', trigger: 'blur'}
                ],
                password: [
                    {required: true, message: '请输入密码', trigger: 'blur'}
                ]
            }
        }
    },
    methods: {
        // 2021-2-24 mjh 修改login方法
        // 增加向后端发送数据验证登录信息环节
        async login(formName) {
            await this.$refs[formName].validate(async (valid) => {
                if (valid) {
                    Global.userName = this.ruleForm.name
                    Global.userPwd = this.ruleForm.password
                    const res =await signInAPI({
                        name: Global.userName,
                        pwd: Global.userPwd,
                    })
                    console.log(res);
                    if (res) {
                        Global.isAuthenticated = true
                        this.$router.push('/homepage')
                    } else {
                        this.$notify.error({
                            title: '错误',
                            message: '用户名或密码错误'
                        });
                    }
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },

        toSignUp() {
            this.$router.push('/signup')
        }
    },
    components: {
        Heading_1,
        BackGround,
        // Heading_2
    }
}
</script>

<style>

.el-button {
    color: rgb(0, 0, 0);
    background: rgba(0, 0, 0, 0.25);
    font-size: 15px;
    font-weight: bold;
    width: 30%;
}

</style>

<style scoped>
.div-background-image {
    width: 100%;
    position: fixed;
    background-image: url("../assets/1542.jpg");
    /* background-image: url("../assets/background.jpg"); */
    background-position: center center;
    background-repeat: no-repeat;
    background-size: cover;
    height: 100%;
}

.div-homepage {
    position: center;
    margin: auto;
    width: 1440px;
    height: 617px;
}

.div-logo {
    width: 130px;
    height: 130px;
    display: inline-block;
    position: relative;
    top: 10px;
    left: -475px;
}

.logo-img {
    margin: auto;
    width: 131.58px;
    height: 164.74px;
    position: relative;
    top: 15px;
}

.div-more-link {
    width: 150px;
    height: 30px;
    margin: auto;
    position: relative;
    top: 30px;
    right: -450px;
    display: inline-block;
}

.link-text {
    display: inline-block;
    border-radius: 15px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    width: 80px;
    height: 30px;
    background: rgba(255, 254, 254, 0.4);
    margin-top: 25px;
    margin-left: auto;
    margin-right: auto;
}

.div-choose {
    width: 800px;
    height: 230px;
    margin-top: 5px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 10px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    background: rgba(0, 0, 0, 0.20);
    padding: 2% 15% 0%;
}

.title {
    border-radius: 12px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.3);
    width: 800px;
    height: 60px;
    background: rgba(0, 0, 0, 0.1);
    margin-top: 25px;
    margin-left: auto;
    margin-right: auto;
    font-weight: bold;
    font-size: 40px;
}


</style>
