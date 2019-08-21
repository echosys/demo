package com.onlinebanking.controller;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.security.Principal;
import java.text.SimpleDateFormat;
import java.util.*;

import com.google.common.io.ByteStreams;
import com.onlinebanking.config.Role;
import com.onlinebanking.config.Role;
import com.onlinebanking.service.AdminService;
import com.onlinebanking.service.TransactionService;
import com.onlinebanking.service.UserService;
import com.onlinebanking.service.UserServiceImpl.AdminServiceImpl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import org.springframework.transaction.annotation.Transactional;

import com.onlinebanking.domain.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;
import com.onlinebanking.dao.RoleDao;
import javax.validation.Valid;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.security.Principal;

import com.onlinebanking.domain.PrimaryTransaction;
import com.onlinebanking.domain.SavingsTransaction;
import com.onlinebanking.enums.UserTypes;
import com.onlinebanking.domain.User;
import com.onlinebanking.domain.security.UserRole;
import com.onlinebanking.domain.SavingsAccount;


@Controller
@RequestMapping("/admin")
public class AdminController {

    @Autowired
    UserService userService;

    @Autowired
    AdminServiceImpl adminService;

    @Autowired
    private RoleDao roleDao;

    TransactionService transactionService;

    @RequestMapping("/")
    public String home() {
        return "redirect:/index";
    }

    @Role({"TIER_1_USER_ROLE"})
    @RequestMapping(value = "/T1", method = RequestMethod.GET)
    public String betweenAccounts(Model model) {
        //model.addAttribute("transferFrom", "");
        //model.addAttribute("transferTo", "");
        //model.addAttribute("amount", "");

        return "T1";
    }

    @Role({"TIER_1_USER_ROLE"})
    @RequestMapping(value = "/T1", method = RequestMethod.POST)
    public String betweenAccountsPost(
            // @ModelAttribute("transferFrom") String transferFrom,
            // @ModelAttribute("transferTo") String transferTo,
            // @ModelAttribute("amount") String amount,
            // Principal principal
    ) throws Exception {
        //User user = userService.findByUsername(principal.getName());
        //PrimaryAccount primaryAccount = user.getPrimaryAccount();
        //SavingsAccount savingsAccount = user.getSavingsAccount();
        //transactionService.betweenAccountsTransfer(transferFrom, transferTo, amount, primaryAccount, savingsAccount);

        return "redirect:/userFront";
    }

    @Role({"ADMIN_ROLE"})
    @RequestMapping(value="/list/{page}", method= RequestMethod.GET)
    public ModelAndView list(@PathVariable("page") int page) {
        ModelAndView modelAndView = new ModelAndView("admin_list");
        PageRequest pageable = new PageRequest(page - 1, 15);
        Page<User> helpPage = adminService.getPaginated(pageable);
        int totalPages = helpPage.getTotalPages();
        if(totalPages > 0) {
            List<Integer> pageNumbers = IntStream.rangeClosed(1,totalPages).boxed().collect(Collectors.toList());
            modelAndView.addObject("pageNumbers", pageNumbers);
        }
        modelAndView.addObject("activeCheckList", true);
        modelAndView.addObject("EmployeeList", helpPage.getContent());
        return modelAndView;
    }

    @Role({"TIER_1_USER_ROLE"})
    @RequestMapping(value="T1/list/{page}", method= RequestMethod.GET)
    public ModelAndView list2(@PathVariable("page") int page) {
        ModelAndView modelAndView = new ModelAndView("adminT1_list");
        PageRequest pageable = new PageRequest(page - 1, 15);
        Page<User> helpPage = adminService.getPaginated(pageable);
        Iterator<User> it = helpPage.iterator();
        while (it.hasNext()) {
            User user = (User) it.next();
            if(user.getUserTypeId() == UserTypes.ADMIN.getType() || user.getUserTypeId() == UserTypes.TIER_1.getType() || user.getUserTypeId() == UserTypes.TIER_2.getType() ) {
                it.remove();
            }
        }

        int totalPages = helpPage.getTotalPages();
        if(totalPages > 0) {
            List<Integer> pageNumbers = IntStream.rangeClosed(1,totalPages).boxed().collect(Collectors.toList());
            modelAndView.addObject("pageNumbers", pageNumbers);
        }
        modelAndView.addObject("activeCheckList", true);

        modelAndView.addObject("EmployeeList", helpPage.getContent());
        return modelAndView;
    }

    @Role({"TIER_2_USER_ROLE"})
    @RequestMapping(value="T2/list/{page}", method= RequestMethod.GET)
    public ModelAndView list3(@PathVariable("page") int page) {
        ModelAndView modelAndView = new ModelAndView("adminT2_list");
        PageRequest pageable = new PageRequest(page - 1, 15);
        Page<User> helpPage = adminService.getPaginated(pageable);
        Iterator<User> it = helpPage.iterator();
        while (it.hasNext()) {
            User user = (User) it.next();
            if(user.getUserTypeId() == UserTypes.ADMIN.getType() || user.getUserTypeId() == UserTypes.TIER_1.getType() || user.getUserTypeId() == UserTypes.TIER_2.getType() ) {
                it.remove();
            }
        }

        int totalPages = helpPage.getTotalPages();
        if(totalPages > 0) {
            List<Integer> pageNumbers = IntStream.rangeClosed(1,totalPages).boxed().collect(Collectors.toList());
            modelAndView.addObject("pageNumbers", pageNumbers);
        }
        modelAndView.addObject("activeCheckList", true);

        modelAndView.addObject("EmployeeList", helpPage.getContent());
        return modelAndView;
    }

    @Role({"ADMIN_ROLE"})
    @RequestMapping(value = "/delete", method = RequestMethod.GET)
    @Transactional
    public String recipientDelete(@RequestParam(value = "employeename") String employeename, Model model, Principal principal){

        adminService.deleteEmployeeByName(employeename);

        List<User> employeelist = adminService.findEmployeeList(principal);

        User user = new User();
        //model.addAttribute("user", user);
        model.addAttribute("EmployeeList", employeelist);


        return "redirect:/admin/list/1";
    }
    @Role({"TIER_2_USER_ROLE"})
    @RequestMapping(value = "/T2/delete", method = RequestMethod.GET)
    @Transactional
    public String recipientDelete2(@RequestParam(value = "employeename") String employeename, Model model, Principal principal){

        adminService.deleteEmployeeByName(employeename);

        List<User> employeelist = adminService.findEmployeeList(principal);

        User user = new User();
        //model.addAttribute("user", user);
        model.addAttribute("EmployeeList", employeelist);


        return "redirect:/admin/T2/list/1";
    }

    @Role({"ADMIN_ROLE"})
    @RequestMapping("/logs")
    public String savingsAccount(Model model, Principal principal) {
        //List<PrimaryTransaction> primarylist= transactionService.showPrimaryTransactionList();

        //System.out.println("PrimaryList" +"----------------------" +primarylist);
        // model.addAttribute("PrimaryTransactionList", primarylist);

        //return "transaction_list";
        List<SavingsTransaction> savingsTransactionList = transactionService.findSavingsTransactionList(principal.getName());
        User user = userService.findByUsername(principal.getName());
        SavingsAccount savingsAccount = user.getSavingsAccount();

        model.addAttribute("savingsAccount", savingsAccount);
        model.addAttribute("savingsTransactionList", savingsTransactionList);

        return "savingsAccount";
    }

    // @RequestMapping(value="/edit", method= RequestMethod.POST) //admin
    // public ModelAndView editEmployee(@Valid User user, RedirectAttributes redirectAttributes) {

    //         User newUser = userService.findByUsername(user.getUsername());
    //         if(!user.getUserId().equals(newUser.getUserId()) || !user.getEmail().equals(newUser.getEmail()) | !user.getFirstName().equals(newUser.getFirstName())){
    //             redirectAttributes.addFlashAttribute("message","Cannot edit Id, name & Email!");
    //             return new ModelAndView("redirect:/admin/list/1");
    //         }
    //         if(user.getPhone() == null || !user.getPhone().matches("-?\\d+(\\.\\d+)?") || user.getPhone().length() != 10){
    //             redirectAttributes.addFlashAttribute("message","Contact Number not valid!");
    //             return new ModelAndView("redirect:/admin/list/1");
    //         }
    //         userService.save(user);
    //         redirectAttributes.addFlashAttribute("message","Successfully saved!");

    //     return new ModelAndView("redirect:/admin/list/1");
    // }

    @Role({"ADMIN_ROLE"})
    @RequestMapping(value = "/signup_admin", method = RequestMethod.GET)
    public String signup(Model model) {
        User user = new User();

        model.addAttribute("user", user);

        return "signup_admin";
    }

    @Role({"ADMIN_ROLE"})
    @RequestMapping(value = "/signup_admin", method = RequestMethod.POST)
    public String signupPost(@ModelAttribute("user") User user,  @ModelAttribute("userType") String userType, Model model) {

        System.out.println(" -----------------------------"+ user);
        System.out.println(" -----------enddddddddddddddd");

        if(userService.checkEmailExists(user.getEmail())){
            model.addAttribute("emailExists", true);

            return "signup";
        }else if(userService.checkUsernameExists(user.getUsername())){

            model.addAttribute("usernameExists", true);

            return "signup";
        } else {
            Set<UserRole> userRoles = new HashSet<>();

            System.out.println(" -----------------------------"+ userType);
            if("CUSTOMER".equals(userType)){
                userRoles.add(new UserRole(user, roleDao.findByName("ROLE_USER")));
                user.setUserTypeId(UserTypes.CUSTOMER.getType());
            }
            else if("TIER_1".equals(userType)){
                userRoles.add(new UserRole(user, roleDao.findByName("TIER_1_USER_ROLE")));
                user.setUserTypeId(UserTypes.TIER_1.getType());
            }
            else if("TIER_2".equals(userType)){
                userRoles.add(new UserRole(user, roleDao.findByName("TIER_2_USER_ROLE")));
                user.setUserTypeId(UserTypes.TIER_2.getType());
            }
            else if("ADMIN".equals(userType)){
                user.setUserTypeId(UserTypes.ADMIN.getType());
            }
            else{
                userRoles.add(new UserRole(user, roleDao.findByName("ROLE_USER")));
                user.setUserTypeId(UserTypes.MERCHANT.getType());
            }
            System.out.println(" 3rd time----------------------"+ user);
            userService.createUser(user, userRoles);

            return "redirect:/admin/list/1";
        }
    }



    @Role({"ADMIN_ROLE"})
    @RequestMapping(value = "/syslogs", method = RequestMethod.GET)
    public @ResponseBody
    ResponseEntity<byte[]> getLogFile() {
        String pattern = "yyyy-MM-dd";
        String filePath = System.getProperty("user.dir") + "/log";
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat(pattern);

        byte[] file = null;
        File dir = new File(filePath);
        File[] directoryListing = dir.listFiles();
        String filename = "";
        if (directoryListing != null) {
            for (File child : directoryListing) {
                try {
                    filename = child.getName();
                    InputStream in = new FileInputStream(child.getAbsoluteFile());
                    file = ByteStreams.toByteArray(in);
                    break;
                }
                catch(Exception e) {
                    return new ResponseEntity<>(HttpStatus.NOT_FOUND);
                }
            }
        }

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment;filename=" + filename)
                // Content-Type
                .contentType(MediaType.APPLICATION_OCTET_STREAM) //
                // Content-Lengh
                .contentLength(file.length) //
                .body(file);
    }

    @Role({"ADMIN_ROLE"})
    @RequestMapping(value = "/edit", method = RequestMethod.GET)
    public String profile(@ModelAttribute("employeename") String employeename,Principal principal, Model model) {
        User user = userService.findByUsername(employeename);

        model.addAttribute("user", user);

        return "employee_admin";
    }

    @Role({"ADMIN_ROLE"})
    @RequestMapping(value = "/edit", method = RequestMethod.POST)
    public String profilePost(@ModelAttribute("user") User newUser, Model model,Principal principal) {
        User user = userService.findByUsername(newUser.getUsername());
        user.setUsername(newUser.getUsername());
        user.setFirstName(newUser.getFirstName());
        user.setLastName(newUser.getLastName());
        user.setEmail(newUser.getEmail());
        user.setPhone(newUser.getPhone());

        model.addAttribute("user", user);

        userService.saveUser(user);

        List<User> employeelist = adminService.findEmployeeList(principal);

        //model.addAttribute("user", user);
        model.addAttribute("EmployeeList", employeelist);

        return "redirect:/admin/list/1";
    }
    @Role({"TIER_2_USER_ROLE"})
    @RequestMapping(value = "T2/edit", method = RequestMethod.GET)
    public String profile2(@ModelAttribute("employeename") String employeename,Principal principal, Model model) {
        User user = userService.findByUsername(employeename);

        model.addAttribute("user", user);

        return "employeeT2_admin";
    }

    @Role({"TIER_2_USER_ROLE"})
    @RequestMapping(value = "/T2/edit", method = RequestMethod.POST)
    public String profilePost2(@ModelAttribute("user") User newUser, Model model,Principal principal) {

        User user = userService.findByUsername(newUser.getUsername());
        if(user.getUserTypeId() == UserTypes.CUSTOMER.getType()){
            user.setUsername(newUser.getUsername());
            user.setFirstName(newUser.getFirstName());
            user.setLastName(newUser.getLastName());
            user.setEmail(newUser.getEmail());
            user.setPhone(newUser.getPhone());

            model.addAttribute("user", user);

            userService.saveUser(user);

            List<User> employeelist = adminService.findEmployeeList(principal);

            //model.addAttribute("user", user);
            model.addAttribute("EmployeeList", employeelist);

            return "redirect:/admin/T2/list/1";
        }
             model.addAttribute("Error", "Invalida Operation");
            return "redirect:/admin/T2/list/1";


    }
}